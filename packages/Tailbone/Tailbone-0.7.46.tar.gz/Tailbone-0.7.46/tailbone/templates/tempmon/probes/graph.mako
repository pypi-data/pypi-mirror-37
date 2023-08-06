## -*- coding: utf-8; -*-
<%inherit file="/base.mako" />

<%def name="title()">Temperature Graph</%def>

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.5.0/Chart.bundle.min.js"></script>
  <script type="text/javascript">

    $(function() {

        var ctx = $('#tempchart');

        var chart = new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: "${probe.description}",
                    data: ${json.dumps(readings_data)|n}
                }]
            },
            options: {
                scales: {
                    xAxes: [{
                        type: 'time',
                        time: {unit: 'minute'},
                        position: 'bottom'
                    }]
                }
            }
        });

    });

  </script>
</%def>

<div class="form-wrapper">

  <div class="field-wrapper">
    <label>Appliance</label>
    <div class="field">
      % if probe.appliance:
          <a href="${url('tempmon.appliances.view', uuid=probe.appliance.uuid)}">${probe.appliance}</a>
      % endif
    </div>
  </div>

  <div class="field-wrapper">
    <label>Probe Location</label>
    <div class="field">${probe.location}</div>
  </div>

  <div class="field-wrapper">
    <label>Showing</label>
    <div class="field">
      <select name="showing-window" id="showing-window" auto-enhance="true">
        <option value="last-hour">Last Hour</option>
      </select>
    </div>
  </div>

</div>

<canvas id="tempchart" width="400" height="150"></canvas>
