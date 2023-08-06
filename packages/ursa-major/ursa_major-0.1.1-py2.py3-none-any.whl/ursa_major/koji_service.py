# -*- coding: utf-8 -*-
# Copyright (c) 2018  Red Hat, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Written by Chenxiong Qi <cqi@redhat.com>
#            Qixiang Wan <qwan@redhat.com>

import copy
import concurrent.futures
import json
import koji
import os
import time

from ursa_major.logger import log


KOJI_TASK_RESULTS = {
    'timeout': 0,
    'failed': 1,
    'done': 2,
}


def wait_koji_task_finish(koji_session, task_id, timeout, interval):
    """
    Wait for a koji task to finish or stop until timeout.

    :param task_id: koji task id
    :param timeout: timeout in seconds
    :param interval: sleep interval in seconds
    :return: value in KOJI_TASK_RESULTS
    """
    failed_states = [koji.TASK_STATES['CANCELED'], koji.TASK_STATES['FAILED']]
    done_states = [koji.TASK_STATES['CLOSED']]
    unfinish_states = [koji.TASK_STATES['FREE'],
                       koji.TASK_STATES['OPEN'],
                       koji.TASK_STATES['ASSIGNED']]

    start = time.time()
    while True:
        if (time.time() - start) >= timeout:
            return KOJI_TASK_RESULTS['timeout']

        task_info = koji_session.getTaskInfo(task_id)
        state = task_info['state']
        if state in unfinish_states:
            log.info("Waiting for task %s to finish...", task_id)
            time.sleep(interval)
        elif state in failed_states:
            return KOJI_TASK_RESULTS['failed']
        elif state in done_states:
            return KOJI_TASK_RESULTS['done']
        else:
            raise RuntimeError("Task %s is in unknown state %s",
                               task_id, state)


class KojiService(object):
    def __init__(self, profile, dry_run=False):
        self.profile = profile
        self.dry_run = dry_run
        self.koji_module = koji.get_profile_module(profile)
        session_opts = koji.grab_session_options(self.koji_module.config)
        self.koji_proxy = koji.ClientSession(self.koji_module.config.server,
                                             session_opts)

    def login(self):
        """Authenticate to the hub."""
        if self.koji_proxy.logged_in:
            return

        auth_type = self.koji_module.config.authtype

        has_cert = (
            auth_type is None and
            os.path.isfile(os.path.expanduser(self.koji_module.config.cert)))

        if auth_type == 'ssl' or has_cert:
            self.koji_proxy.ssl_login(
                os.path.expanduser(self.koji_module.config.cert),
                os.path.expanduser(self.koji_module.config.ca),
                os.path.expanduser(self.koji_module.config.serverca))

        elif auth_type == 'kerberos':
            self.koji_proxy.krb_login(
                getattr(self.koji_module.config, 'principal', None),
                getattr(self.koji_module.config, 'keytab', None))
        else:
            raise RuntimeError('Unsupported authentication type in Koji')

    def logout(self):
        """ expire the login session"""
        if self.koji_proxy.logged_in:
            self.koji_proxy.logout()

    def get_tag(self, tag):
        """Get tag info

        :param tag: tag name or ID.
        :type tag: int or str
        :return: the return value from Koji API getTag.
        """
        log.debug('Get tag info: %s', tag)
        return self.koji_proxy.getTag(tag)

    def get_tag_id(self, tag):
        """Get tag id

        :param tag: tag name.
        :type tag: str
        :return: tag id
        """
        taginfo = self.get_tag(tag)
        return taginfo['id']

    def is_build_tag(self, tag):
        """ Check if tag is a build tag

        :param tag: tag name
        :return: return True if tag is a build tag, else False
        """
        if self.get_build_targets(self.get_tag_id(tag)):
            return True
        return False

    def find_build_tags(self, tag):
        """
        Find build tags in tag's children tags
        It stops when reaches the first build tag in each inheritance path.

        :param tag: tag name
        :return: List of tag names
        """
        # To find out the build tags, we check the tag's inheritance data,
        # when it reaches the first build tag in each inheritant path, it
        # stops and return that build tag, and it stops at any tag that name
        # starts with 'module-'.
        #
        # For examples, if we have tag inheritance data as below (tags with
        # '*' marks are build tags):
        #
        # Example #1:
        #     my-example-tag
        #       └─product-foo-temp-override
        #          └─product-foo-override
        #             └─product-foo-build (*)
        #                ├─tmp-product-foo-build (*)
        #                └─alt-product-foo-build (*)
        #
        # Build tags for 'my-example-tag' are: ['product-foo-build']
        #
        # In example #1, we stops at 'product-foo-build', so
        # 'tmp-product-foo-build' and 'alt-product-foo-build' are not checked
        # at all.
        #
        # Example #2:
        #     my-example-tag
        #       ├─module-345678-build
        #       ├─module-234567-build
        #       ├─module-123456-build
        #       │  └─product-foo-module-hotfix
        #       │     └─product-foo-module-hotfix-build (*)
        #       ├─tmp-product-foo-python-candidate
        #       │  └─tmp-product-foo-python-override
        #       │     └─tmp-product-foo-python-build (*)
        #       ├─product-foo-container-build (*)
        #       └─product-foo-temp-override
        #          └─product-foo-override
        #             └─product-foo-build (*)
        #                ├─tmp-product-foo-build (*)
        #                └─alt-product-foo-build (*)
        #
        # Build tags for 'my-example-tag' are:
        #
        #     ['tmp-product-foo-python-build', 'product-foo-container-build',
        #      'product-foo-build']
        #
        # In example #2, 'product-foo-module-hotfix-build' is a build tag, but
        # we doesn't count it in, because we stops at its child tag
        # 'module-123456-build'.

        tag_id = self.get_tag_id(tag)

        inheritance = self.koji_proxy.getFullInheritance(tag_id, reverse=True)
        # sort the tags by depth, so we can check tags will lower depth first
        # and if a tag match the condition which we will stop, we can add it
        # in blocked tags, then it's children (which has higher depth) will
        # not be checked either.
        sorted_inheritance = sorted(inheritance, key=lambda x: x['currdepth'])

        build_tags = []

        # check whether a tag is build tag, but not check tags that:
        # 1. tag name starts with 'module-'
        # 2. its parent tag is in blocked_tags
        blocked_tags = []

        for tag in sorted_inheritance:
            parent = tag['parent_id']
            if parent in blocked_tags:
                blocked_tags.append(tag['tag_id'])
                continue

            # ignore all 'module-*' tags and don't continue with their children
            if tag['name'].startswith('module-'):
                blocked_tags.append(tag['tag_id'])
                continue

            log.info("Checking whether '%s' is a build tag", tag['name'])
            if self.is_build_tag(tag['name']):
                blocked_tags.append(tag['tag_id'])
                build_tags.append(tag['name'])
        return build_tags

    def get_inheritance_data(self, tag, full=False):
        """Get koji tag inheritance data

        :param tag: tag name or id
        :param full: if true, this will return the full inheritance data
        """
        if full:
            return self.koji_proxy.getFullInheritance(tag)
        return self.koji_proxy.getInheritanceData(tag)

    def set_inheritance_data(self, tag, data):
        """Set inheritance data

        :param tag: tag name passed into the first argument of
            `setInheritanceData`.
        :param data: list of mappings passed into the second argument of
            `setInheritanceData`.
        """
        if self.dry_run:
            log.info('DRY RUN: set inheritance data for tag %s: %s',
                     tag, json.dumps(data, indent=2))
        else:
            return self.koji_proxy.setInheritanceData(tag, data)

    def update_tag_inheritance(self, tag, add_tags=None, remove_tags=None, edit_tags=None):
        """Update tag inheritance data with specified data of tags.

        :param tag:         id or name of child tag
        :param add_tags:    list of parent tags to be added, each tag is a
                            dict containing at least tag name or id
        :param remove_tags: list of tags to be removed, each tag is a dict
                            containing at least tag name or id
        :param edit_tags:   list of tags to be edited, each tag is a dict
                            containing at least tag name or id, and tags in
                            list should already exist in inheritance data
        """
        child_tag = self.get_tag(tag)
        if not child_tag:
            raise RuntimeError("Unknown koji tag: {}".format(tag))

        if add_tags is None and remove_tags is None and edit_tags is None:
            log.info("There is no update data specified for updating tag "
                     "inheritance of '%s', do nothing", tag)
            return

        inheritance_data = self.get_inheritance_data(child_tag['id'])

        # update inheritance data for tags need to be removed or updated
        # do this before add new parent tags because we can add tags
        # to replace some old tags with the same priority

        # remove tags are also tags to be edited, we add these tags to
        # edit_tags, then handle them in the similar way

        if edit_tags is None:
            edit_tags = []

        if remove_tags is None:
            remove_tags = []
        for remove_tag in remove_tags:
            edit_tags.append(remove_tag)

        if edit_tags:
            for tag in edit_tags:
                tag_name_or_id = tag.get('name') or tag.get('id')
                edit_tag = self.get_tag(tag_name_or_id)
                if not edit_tag:
                    raise RuntimeError("Tag {} doesn't exist".format(tag_name_or_id))

                data = [d for d in inheritance_data
                        if d['parent_id'] == edit_tag['id']]

                if len(data) == 0:
                    msg = "Tag {} not found in inheritance.".format(edit_tag['name'])
                    log.error(msg)
                    raise RuntimeError(msg)
                if len(data) > 1:
                    msg = "Multiple tag {} found in inheritance".format(edit_tag['name'])
                    log.error(msg)
                    raise RuntimeError(msg)

                data = data[0]

                edit_data = data.copy()
                if tag in remove_tags:
                    edit_data['delete link'] = True
                else:
                    valid_keys = ['priority', 'maxdepth', 'intransitive',
                                  'noconfig', 'pkg_filter']
                    for key in valid_keys:
                        if key in tag.keys():
                            edit_data[key] = tag.get(key)

                    same_priority = [d for d in inheritance_data if
                                     d['priority'] == edit_data['priority'] and
                                     not d.get('delete link', False) and
                                     d['name'] != edit_tag['name']]
                    if same_priority:
                        msg = ("Tag {} has an inheritance with the same priority "
                               "{} as tag {}".format(child_tag['name'],
                                                     edit_data['priority'],
                                                     edit_tag['name']))
                        log.error(msg)
                        raise RuntimeError(msg)

                index = inheritance_data.index(data)
                # update the tag to be edited with updated tag data
                inheritance_data[index] = edit_data

        if add_tags is not None:
            # update inheritance data for tags need to be added
            for tag in add_tags:
                add_tag = self.get_tag(tag.get('name') or tag.get('id'))
                if not add_tag:
                    raise RuntimeError("Tag {} doesn't exist".format(tag))

                add_data = {}
                add_data['parent_id'] = add_tag.get('id')
                add_data['priority'] = tag.get('priority', 0)
                add_data['maxdepth'] = tag.get('maxdepth', None)
                add_data['intransitive'] = tag.get('intransitive', False)
                add_data['noconfig'] = tag.get('noconfig', False)
                add_data['pkg_filter'] = tag.get('pkg_filter', '')

                same_priority = [d for d in inheritance_data if
                                 d['priority'] == add_data['priority'] and
                                 not d.get('delete link', False)]
                if same_priority:
                    # TODO: should we raise error or just warn
                    msg = ("Tag {} has an inheritance with the same priority "
                           "{} as tag {}".format(child_tag['name'],
                                                 add_data['priority'],
                                                 add_tag['name']))
                    log.warn(msg)

                same_parent = [d for d in inheritance_data if
                               d['parent_id'] == add_data['parent_id'] and
                               not d.get('delete link', False)]
                if same_parent:
                    raise RuntimeError(
                        "Tag %s already exists in tag %s's inheritance" %
                        (add_tag['name'], child_tag['name']))

                inheritance_data.append(add_data)

        log.info(
            'Update inheritance of tag %s with inheritance data: %s',
            child_tag['name'], json.dumps(inheritance_data, indent=2))
        self.set_inheritance_data(child_tag['id'], inheritance_data)

    def remove_tags_from_inheritance(self, tag, tags):
        """ Remove tags from a tag's inheritance data.

        :param tag: tag name, the child tag where we get the inheritance data
        :param tags: a list of tag names
        """
        inheritance = self.get_inheritance_data(tag)
        for remove_tag in tags:
            taginfo = self.get_tag(remove_tag)
            data = [d for d in inheritance
                    if d['parent_id'] == taginfo['id']]
            if len(data) == 0:
                raise RuntimeError("Tag {} is not in tag {}'s inheritance"
                                   .format(remove_tag, tag))
            data = data[0]
            remove_data = copy.deepcopy(data)
            remove_data['delete link'] = True
            index = inheritance.index(data)
            inheritance[index] = remove_data

        msg = ("{}Removing tags {!r} from tag {}'s inheritance"
               .format("DRYRUN: " if self.dry_run else "", tags, tag))
        log.info(msg)
        if not self.dry_run:
            self.login()
            self.set_inheritance_data(tag, inheritance)

    def get_build_targets(self, build_tag_id):
        """
        Get build targets of a tag.

        :param build_tag_id: tag id
        :return: return value from koji's getBuildTargets API
        """
        if self.dry_run:
            log.info("DRY RUN: Getting build target for tag %s",
                     build_tag_id)
            return []
        return self.koji_proxy.getBuildTargets(buildTagID=build_tag_id)

    def regen_repo(self, tag, debuginfo=False, src=False, wait=False):
        """
        Regenarate a repo.

        :param tag: tag name or tag id
        :param debuginfo: include debuginfo rpms in repo or not
        :param src: include source rpms in repo or not
        """
        taginfo = self.get_tag(tag)
        if not taginfo:
            msg = "Tag {} not found".format(tag)
            log.error(msg)
            raise RuntimeError(msg)

        tagid = taginfo['id']
        tagname = taginfo['name']
        if not taginfo['arches']:
            log.warn("Warning: tag %s has an empty arch list", tagname)

        targets = self.get_build_targets(tagid)
        if not targets:
            log.warn("Warning: %s is not a build tag", tagname)

        repo_opts = {}
        if debuginfo:
            repo_opts['debuginfo'] = True
        if src:
            repo_opts['src'] = True

        if self.dry_run:
            log.info("DRY RUN: Regenerating repo for tag: %s", tagname)
            return None

        try:
            task_id = self.koji_proxy.newRepo(tagname, **repo_opts)
        except Exception as e:
            raise RuntimeError("Failed to create regenerate repo task: %s" % str(e))
        task_url = "{}/taskinfo?taskID={}".format(
            self.koji_module.config.weburl, task_id)
        log.info("Regenerating repo for tag: %s", tagname)
        log.info("Created task: %d", task_id)
        log.info("Task info: %s", task_url)
        if not wait:
            return

        state = wait_koji_task_finish(self.koji_proxy, task_id,
                                      timeout=30 * 60, interval=10)
        if state == KOJI_TASK_RESULTS['timeout']:
            msg = "Timeout while waiting task {} to finish".format(task_id)
            raise RuntimeError(msg)
        elif state == KOJI_TASK_RESULTS['failed']:
            msg = "Task {} failed, check task url {} for details".format(
                task_id, task_url)
            raise RuntimeError(msg)
        elif state == KOJI_TASK_RESULTS['done']:
            log.info("Task %s succeed, repo of tag %s is re-generated",
                     task_id, tagname)

    def regen_repos(self, tags, debuginfo=False, src=False, wait=False):
        """
        Regenerate repos of tags

        :param tags: list of tag names
        :return: None
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(tags)) as executor:
            to_regen = {
                executor.submit(self.regen_repo, tag, debuginfo=debuginfo, src=src, wait=wait):
                tag for tag in tags
            }
            for future in concurrent.futures.as_completed(to_regen):
                tag = to_regen[future]
                try:
                    future.result()
                except Exception as exc:
                    log.warn("Error while re-generating repo for %s: %s", tag, str(exc))
                else:
                    if not wait:
                        log.info("Regen-repo task of tag %s is created", tag)
                    else:
                        log.info("Repo of %r is re-generated", tag)
