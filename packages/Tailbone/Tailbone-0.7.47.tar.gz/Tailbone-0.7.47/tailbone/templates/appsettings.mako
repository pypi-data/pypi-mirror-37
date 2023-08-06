## -*- coding: utf-8; -*-
<%inherit file="/base.mako" />

<%def name="title()">App Settings</%def>

<%def name="content_title()"></%def>

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  ${h.javascript_link(request.static_url('tailbone:static/js/tailbone.appsettings.js') + '?ver={}'.format(tailbone.__version__))}
</%def>

<%def name="extra_styles()">
  ${parent.extra_styles()}
  <style type="text/css">
    div.form {
        float: none;
    }
    div.panel {
        width: 85%;
    }
    .field-wrapper {
        margin-bottom: 2em;
    }
    .panel .field-wrapper label {
        font-family: monospace;
        width: 50em;
    }
  </style>
</%def>

<div class="form">
  ${h.form(form.action_url, id=dform.formid, method='post', class_='autodisable')}
  ${h.csrf_token(request)}

  % if dform.error:
      <div class="error-messages">
        <div class="ui-state-error ui-corner-all">
          <span style="float: left; margin-right: .3em;" class="ui-icon ui-icon-alert"></span>
          Please see errors below.
        </div>
        <div class="ui-state-error ui-corner-all">
          <span style="float: left; margin-right: .3em;" class="ui-icon ui-icon-alert"></span>
          ${dform.error}
        </div>
      </div>
  % endif

  <div class="group-picker">
    <div class="field-wrapper">
      <label for="settings-group">Showing Group</label>
      <div class="field">
        ${h.select('settings-group', current_group, group_options, **{'auto-enhance': 'true'})}
      </div>
    </div>
  </div>

  % for group in groups:
      <div class="panel" data-groupname="${group}">
        <h2>${group}</h2>
        <div class="panel-body">

          % for setting in settings:
              % if setting.group == group:
                  <% field = dform[setting.node_name] %>

                  <div class="field-wrapper ${field.name} ${'with-error' if field.error else ''}">
                    % if field.error:
                        <div class="field-error">
                          % for msg in field.error.messages():
                              <span class="error-msg">${msg}</span>
                          % endfor
                        </div>
                    % endif
                    <div class="field-row">
                      <label for="${field.oid}">${form.get_label(field.name)}</label>
                      <div class="field">
                        ${field.serialize()|n}
                      </div>
                    </div>
                    % if form.has_helptext(field.name):
                        <span class="instructions">${form.render_helptext(field.name)}</span>
                    % endif
                  </div>
              % endif
          % endfor

        </div><!-- panel-body -->
      </div><! -- panel -->
  % endfor

  <div class="buttons">
    ${h.submit('save', getattr(form, 'submit_label', getattr(form, 'save_label', "Submit")))}
    ${h.link_to("Cancel", form.cancel_url, class_='cancel button{}'.format(' autodisable' if form.auto_disable_cancel else ''))}
  </div>

  ${h.end_form()}
</div>
