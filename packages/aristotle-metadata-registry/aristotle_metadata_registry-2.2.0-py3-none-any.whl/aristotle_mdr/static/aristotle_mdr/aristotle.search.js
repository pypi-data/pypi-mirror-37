function showClearFilters() {
    $("#advanced_nav_link").addClass("clearFilters")
    $("#advanced_label").hide();
    $("#clear_filters").show();
}

function hideClearFilters() {
    $("#advanced_nav_link").removeClass("clearFilters")
    $("#advanced_label").show();
    $("#clear_filters").hide();
}

function clearFilters() {
    $(".searchAdvanced input:checked").each( function() {
        $(this).prop("checked", false);
    });
    $(".searchAdvanced .badge").text('');
    $(".searchAdvanced .details").text('');
}

function checkFilters() {
    // Disgregard "any time" filters.
    x = $(".searchAdvanced input:checked[value != 'a']").length;
    y = 0
    if (x==0) {
        y = $(".searchAdvanced .date input[type='text']").each( function() {
            if (this.value) {
                y++;
                //console.log(this);
            }
        });
    }
    //console.log(x,y);
    if ( (x+y) > 0) {
        showClearFilters();
    } else {
        hideClearFilters();
    }
}

function updateCheckboxBadge(menu) {
    x = $(menu).find("input:checked").length;
    if (x > 0) {
        $(menu).parent().find(".badge").text(x);
    } else {
        $(menu).parent().find(".badge").text('');
    }
    checkFilters();
}

function clearCustomDates(menu) {
    $(menu).find("input[type='text']").each(function() {
        this.value = "";
    });
}

function updateDateRadioDetails(menu) {
    x = $(menu).find("input:checked");
    if (x.length > 0 && x[0].value != 'a') {
        x=x[0];
        $(menu).parent().find(".details").text($("label[for='"+x.id+"']").text());
    } else {
        $(menu).parent().find(".details").text('');
    }
    checkFilters();
}
function updateSortRadioDetails(menu) {
    x = $(menu).find("input:checked");
    if (x.length == 0 ) {
        x = $(menu).find("input[value='n']");
        x.prop("checked", true);
    }
    x=x[0];
    $(menu).parent().find(".details").text($("label[for='"+x.id+"']").text());
}

$( document ).ready( function() {
    $('.dropdown-menu-date .date').on('click', function(e) {
        e.stopPropagation();
    });

    $('.dropdown-menu-form .dropdown-menu').on('click', function(e) {
        e.stopPropagation();
        updateCheckboxBadge(this);
    });

    $('.dropdown-menu-form .dropdown-menu').each( function() {
        updateCheckboxBadge(this);
    });

    $('.dropdown-menu-date input[type=text]').on('click', function(e) {
        e.stopPropagation();
    });


    $('.dropdown-menu-date .dropdown-menu').on('click', function(e) {
        updateDateRadioDetails(this);
        clearCustomDates(this);
    });

    $('.dropdown-menu-date .dropdown-menu').each( function() {
        updateDateRadioDetails(this);
    });

    // Setup the sort ordering box
    $('.sort-order-box .dropdown-menu').on('click', function(e) {
        e.stopPropagation();
        updateSortRadioDetails(this);
        $(this).closest("form").submit();
    });
    $('.sort-order-box .dropdown-menu').each( function() {
        updateSortRadioDetails(this);
    });

    // Setup the advance/clear toggle button in the navbar
    $('#advanced_nav_link').on('click', function(e) {
        if ($(this).hasClass("clearFilters")) {
            clearFilters();
            clearCustomDates();
            hideClearFilters();
        }
    });

    // When a custom date changes, auto-tick the custom range box
    $('.dropdown-menu-date .dropdown-menu .input-group.date').each( function() {
        $(this).on("dp.change", function() {
            $(this).parents(".dropdown-menu").first().find("[value='X']").prop("checked", true);
        });
    });


    $("#search-input").keydown(function(e){
        if(e.which == 13) { // enter
            setTimeout(function(){
                $(".search-option:first").focus();
            },100);
        }
    });

    $(".dropdown-menu-form").keydown(function(e){
        if(e.keyCode == 40) { // down
            $(this).find("a").click();
            $(this).find("label").first().focus();
            return false; // stops the page from scrolling
        }
     });

    $(".dropdown-menu-form .dropdown-menu li").keydown(function(e){
        if(e.keyCode == 40) { // down
            $(this).next().find("label").focus();
            return false; // stops the page from scrolling
        }
        if(e.keyCode == 38) { // up
            $(this).prev().find("label").focus();
            return false; // stops the page from scrolling
        }
        if(e.keyCode == 13) { // enter
            $(this).find("label").click();
            return false; // stops the page from scrolling
        }
    });

    //Results Per Page Functionality

    //set appropriate button to primary
    var set = false;
    $('.rpp').each(function() {
      var current_rpp = $('#id_rpp').val()
      if ($(this).val().valueOf() == current_rpp) {
        $(this).addClass('btn-primary');
        $(this).removeClass('btn-default');
        set = true;
      }
    });

    if (set == false) {
      $('#default_rpp').addClass('btn-primary')
      $('#default_rpp').removeClass('btn-default')
    }

    //on button click update hidden field
    $('.rpp').click(function() {
      var new_rpp = $(this).val();
      $('#id_rpp').val(new_rpp);
      $('#search_form').submit();
    });



});
