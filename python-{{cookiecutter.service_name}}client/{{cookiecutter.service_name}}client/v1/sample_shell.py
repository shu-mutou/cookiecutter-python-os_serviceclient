# Copyright 2013 Red Hat, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from {{cookiecutter.service_name}}client.common import utils
from {{cookiecutter.service_name}}client.openstack.common import cliutils
from {{cookiecutter.service_name}}client.v1 import resource_fields as res_fields


def _print_sample_show(sample):
    fields = ['uuid', 'description', 'created_at', 'updated_at', 'extra']
    data = dict([(f, getattr(sample, f, '')) for f in fields])
    cliutils.print_dict(data, wrap=72)


@cliutils.arg('sample', metavar='<sample>', help="UUID of the sample.")
def do_sample_show(cc, args):
    """Show detailed information about a sample."""
    utils.check_empty_arg(args.sample, '<sample>')
    sample = cc.sample.get(args.sample)
    _print_sample_show(sample)


@cliutils.arg(
    '--detail',
    dest='detail',
    action='store_true',
    default=False,
    help="Show detailed information about the sample.")
@cliutils.arg(
    '--limit',
    metavar='<limit>',
    type=int,
    help='Maximum number of sample to return per request, '
         '0 for no limit. Default is the maximum number used '
         'by the {{cookiecutter.service_name|capitalize}} API Service.')
@cliutils.arg(
    '--sort-key',
    metavar='<field>',
    help='Sample field that will be used for sorting.')
@cliutils.arg(
    '--sort-dir',
    metavar='<direction>',
    choices=['asc', 'desc'],
    help='Sort direction: "asc" (the default) or "desc".')
def do_sample_list(cc, args):
    """List the sample."""
    if args.detail:
        fields = res_fields.SAMPLE_DETAILED_RESOURCE.fields
        field_labels = res_fields.SAMPLE_DETAILED_RESOURCE.labels
        sort_fields = res_fields.SAMPLE_DETAILED_RESOURCE.sort_fields
        sort_field_labels = res_fields.SAMPLE_DETAILED_RESOURCE.sort_labels
    else:
        fields = res_fields.SAMPLE_RESOURCE.fields
        field_labels = res_fields.SAMPLE_RESOURCE.labels
        sort_fields = fields
        sort_field_labels = field_labels

    params = utils.common_params_for_list(args, sort_fields,
                                          sort_field_labels)

    sample = cc.sample.list(**params)
    cliutils.print_list(sample, fields,
                        field_labels=field_labels,
                        sortby_index=None)


@cliutils.arg(
    '-d', '--description',
    metavar='<description>',
    help='Description of the sample.')
@cliutils.arg(
    '-e', '--extra',
    metavar="<key=value>",
    action='append',
    help="Record arbitrary key/value metadata. "
         "Can be specified multiple times.")
def do_sample_create(cc, args):
    """Create a new sample."""
    field_list = ['description', 'extra']
    fields = dict((k, v) for (k, v) in vars(args).items()
                  if k in field_list and not (v is None))
    fields = utils.args_array_to_dict(fields, 'extra')
    sample = cc.sample.create(**fields)

    field_list.append('uuid')
    data = dict([(f, getattr(sample, f, '')) for f in field_list])
    cliutils.print_dict(data, wrap=72)


@cliutils.arg(
    'sample',
    metavar='<sample>',
    nargs='+',
    help="UUID of the sample.")
def do_sample_delete(cc, args):
    """Delete a sample."""
    for c in args.sample:
        cc.sample.delete(c)
        print('Deleted sample %s' % c)


@cliutils.arg('sample', metavar='<sample>', help="UUID of the sample.")
@cliutils.arg(
    'op',
    metavar='<op>',
    choices=['add', 'replace', 'remove'],
    help="Operation: 'add', 'replace', or 'remove'.")
@cliutils.arg(
    'attributes',
    metavar='<path=value>',
    nargs='+',
    action='append',
    default=[],
    help="Attribute to add, replace, or remove. Can be specified "
         "multiple times. For 'remove', only <path> is necessary.")
def do_sample_update(cc, args):
    """Update information about a sample."""
    patch = utils.args_array_to_patch(args.op, args.attributes[0])
    sample = cc.sample.update(args.sample, patch)
    _print_sample_show(sample)


@cliutils.arg(
    '--detail',
    dest='detail',
    action='store_true',
    default=False,
    help="Show detailed information about the childlen.")
@cliutils.arg(
    '--limit',
    metavar='<limit>',
    type=int,
    help='Maximum number of childlen to return per request, '
         '0 for no limit. Default is the maximum number used '
         'by the {{cookiecutter.service_name|capitalize}} API Service.')
@cliutils.arg(
    '--sort-key',
    metavar='<field>',
    help='Child field that will be used for sorting.')
@cliutils.arg(
    '--sort-dir',
    metavar='<direction>',
    choices=['asc', 'desc'],
    help='Sort direction: "asc" (the default) or "desc".')
@cliutils.arg('sample', metavar='<sample>', help="UUID of the sample.")
def do_sample_child_list(cc, args):
    """List the childlen contained in a sample."""
    if args.detail:
        fields = res_fields.NODE_DETAILED_RESOURCE.fields
        field_labels = res_fields.NODE_DETAILED_RESOURCE.labels
    else:
        fields = res_fields.NODE_RESOURCE.fields
        field_labels = res_fields.NODE_RESOURCE.labels

    params = utils.common_params_for_list(args, fields, field_labels)

    childlen = cc.sample.list_childlen(args.sample, **params)
    cliutils.print_list(childlen, fields,
                        field_labels=field_labels,
                        sortby_index=None)
