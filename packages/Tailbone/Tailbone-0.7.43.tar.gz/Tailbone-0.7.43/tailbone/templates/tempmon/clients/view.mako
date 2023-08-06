## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

<%def name="head_tags()">
  ${parent.head_tags()}
  <script type="text/javascript">
    $(function() {
        $('#restart-client').click(function() {
            disable_button(this);
            location.href = '${url('tempmon.clients.restart', uuid=instance.uuid)}';
        });
    });
  </script>
</%def>

<ul id="context-menu">
  ${self.context_menu_items()}
</ul>

% if instance.enabled and master.restartable_client(instance) and request.has_perm('{}.restart'.format(route_prefix)):
    <div class="object-helper">
      <h3>Client Tools</h3>
      <div class="object-helper-content">
        <button type="button" id="restart-client">Restart tempmon-client daemon</button>
      </div>
    </div>
% endif

<div class="form-wrapper">
  ${form.render()|n}
</div><!-- form-wrapper -->

% if master.has_rows:
    ${rows_grid|n}
% endif
