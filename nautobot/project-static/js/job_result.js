var url = nautobot_api_path + "extras/job-results/";
var timeout = 1000;

function updatePendingStatusLabel(status){
    var labelClass;
    if (status.value === 'failed' || status.value === 'errored'){
        labelClass = 'danger';
    } else if (status.value === 'running'){
        labelClass = 'warning';
    } else if (status.value === 'completed'){
        labelClass = 'success';
    } else {
        labelClass = 'default';
    }
    var elem = $('#pending-result-label > label');
    elem.attr('class', 'label label-' + labelClass);
    elem.text(status.label);
}

function refreshWindow(){
    window.location.reload();
}

$(document).ready(function(){
    if (pending_result_id !== null){
        (function checkPendingResult(){
            $.ajax({
                url: url + pending_result_id + '/',
                method: 'GET',
                dataType: 'json',
                context: this,
                success: function(data) {
                    updatePendingStatusLabel(data.status);
                    setTimeout(jobTerminatedAction, 1000);
                }
            });
        })();
    }
})
