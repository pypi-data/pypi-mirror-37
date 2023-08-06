## -*- coding: utf-8; -*-
<%inherit file="/batch/view.mako" />

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  % if request.has_perm('{}.edit_row'.format(permission_prefix)):
      <script type="text/javascript">

        $(function() {

            $('.grid-wrapper').on('click', '.grid .actions a.transform', function() {

                var form = $('form[name="transform-unit-form"]');
                var row_uuid = $(this).parents('tr:first').data('uuid');
                form.find('[name="row_uuid"]').val(row_uuid);

                $.get(form.attr('action'), {row_uuid: row_uuid}, function(data) {

                    if (typeof(data) == 'object') {
                        alert(data.error);

                    } else {
                        $('#transform-unit-dialog').html(data);
                        $('#transform-unit-dialog').dialog({
                            title: "Transform Pack to Unit Item",
                            width: 800,
                            height: 450,
                            modal: true,
                            buttons: [
                                {
                                    text: "Transform",
                                    click: function(event) {
                                        disable_button(dialog_button(event));
                                        form.submit();
                                    }
                                },
                                {
                                    text: "Cancel",
                                    click: function() {
                                        $(this).dialog('close');
                                    }
                                }
                            ]
                        });
                    }
                });

                return false;
            });

        });

      </script>
  % endif
</%def>

${parent.body()}

% if request.has_perm('{}.edit_row'.format(permission_prefix)):
    ${h.form(url('{}.transform_unit_row'.format(route_prefix), uuid=batch.uuid), name='transform-unit-form')}
    ${h.csrf_token(request)}
    ${h.hidden('row_uuid')}
    ${h.end_form()}

    <div id="transform-unit-dialog" style="display: none;">
      <p>hello world</p>
    </div>
% endif
