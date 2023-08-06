// Set (then unset) this to supress the ajax loading animation
var suppressLoadingBlock = false;

function clearMessages() {
  var message_list = $('#messages-row').find('ul').html('')
}

function clearAndHideMessages() {
  clearMessages()
  var row = $('#messages-row').attr('hidden', '')
}

function addHeaderMessage(message) {
  clearMessages()
  var row = $('#messages-row')
  row.find('.alert').removeAttr('hidden')
  var message_list = row.find('ul')
  var element = $('<li>', {text: message})
  message_list.append(element)
}

// getCookie function taken from django docs
// Used to get csrf_token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function() {
    // Scrap modals if they lose focus so they can be loaded with new content
    $('.modal').on('hidden.bs.modal', function(e)
    {
        if (!$(this).hasClass('exclude-scrap')) {
          $(this).removeData();
          x = $(this).find('.modal-content > *');
          //console.log(x)
          x.remove()
        }
    });

    $('.modal').on('loaded.bs.modal', function() {
        // Need to do this on modal show for newly added popovers
        $('.aristotle-popover').popover()
    });

    // Initialize popovers
    $('.aristotle-popover').popover()

    $('#messages-row').find('.close').click(clearAndHideMessages)

    //Initialise delete checkboxes
    $('.delete-disable').click(function() {
      var deletebox = $(this)
      var checked = deletebox.prop('checked')
      var form = deletebox.closest('form')
      form.find('input').each(function() {
        if ($(this).attr('id') != deletebox.attr('id') && $(this).attr('name') != 'csrfmiddlewaretoken') {
          $(this).prop('disabled', checked)
        }
      })
      form.find('.widget-button').each(function() {
        $(this).prop('disabled', checked)
      })
    })

});

$(document).ajaxSend(function(event, request, settings) {
    if (!suppressLoadingBlock) {
        $('#loading_indicator').show().addClass('loading').removeClass('hidden');
    }
});

$(document).ajaxComplete(function(event, request, settings) {
    $('#loading_indicator').hide().removeClass('loading');
});
