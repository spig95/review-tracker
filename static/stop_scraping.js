function get_and_clean_running_scrape_task_id() {
    if ($('#scrape_tid').length > 0) {
        var tid = $('#scrape_tid').data("scrape-tid");
        $('#scrape_tid').removeData("scrape-tid");
        return tid;
    } else {
        return null;
    }
}

function stop_scraping(){
    stop_show_results_with_ajax();  // Stops to execute the get results function
    $.ajax('/api/stop_scraping_and_get_partial_results',   // request url
    {
        data: {
            task_to_kill: get_and_clean_running_scrape_task_id()
        },
        dataType: "json", // return type of request
        success: function(ret) {
            show_scrape_result(ret.graph, ret.info_str, ret.is_result_final);

        },
        error: function () { // error callback function
            $('#results_graph').html("Can't find results.");
        }
    });
}


$(function(){
    $('#kill_task_btn').click(function() {
        $('#kill_task_div').addClass('not-visible'); // Todo: use fadeout?
        stop_scraping();
    });
});
