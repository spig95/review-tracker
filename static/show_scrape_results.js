var early_stop = false;

function get_running_scrape_task_id() {
    if ($('#scrape_tid').length > 0) {
        var tid = $('#scrape_tid').data("scrape-tid");
        return tid;
    } else {
        return null;
    }
}

function stop_show_results_with_ajax() {
    early_stop = true;
}

function show_results_with_ajax(){
    var call_again = true;
    if (early_stop) {
        call_again = false;
    }
    $.ajax('/api/get_scrape_task_results',   // request url
    {
        data: {
            running_task_id: get_running_scrape_task_id()
        },
        dataType: "json", // return type of request
        success: function(ret) {
            show_scrape_result(ret.graph, ret.info_str, ret.is_result_final);
            if (ret.is_result_final == true) {
                call_again = false;
            }
        },
        error: function () { // error callback function
            $('#results_graph').html("Can't find results.");
        },
        complete: function() { // complete (after error/success) callback function
            if (call_again) {
                setTimeout(show_results_with_ajax, 3000);
            }
        }
    });
}


function show_scrape_result(graph, info_str, is_result_final) {
    if (is_result_final == true) {
        hide_stop_button();
        aux_fading("#results_str", "Reviews over time");
    } else if (early_stop) {
        hide_stop_button();
        aux_fading("#results_str", "Reviews over time (Interrupted)");
    } else {
        // No Fading here
        show_stop_button();
        $("#results_str").html("Reviews over time (in progress)");
    };
    aux_fading("#info_str", info_str); //$('#info_str').html(info_str);
    $('#results_graph').html(graph);
    //aux_fading("#results_graph", graph); //
}


function show_stop_button() {
    if ($('#kill_task_div').hasClass('not-visible')) {
        $('#kill_task_div').removeClass('not-visible');
    };
}


function hide_stop_button() {
    $("#kill_task_div").fadeOut();
}

/**
 * One liner to replace content with fade-out old content and fade-in new content.
 * @param  {String} selector     Selector for the element
 * @param  {String} html_content This content will replace the previous one of the selected element
 */
function aux_fading(selector_str, html_content) {
    $(selector_str).fadeOut(function() {
      $(this).html(html_content)
    }).fadeIn();
}

// Trigger the function showing results if there is one running task ID
$(function(){
    if (get_running_scrape_task_id() !== null) {
        show_results_with_ajax();
    }
});


// Trigger the function showing results if the button is pressed
$(function(){
    $('#start_scrape_task').click(function() {
        early_stop = false;
        show_results_with_ajax();
    });
});
