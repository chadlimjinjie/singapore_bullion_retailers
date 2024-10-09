(function() {

//Common for all pages 

    $('#signup-btn').click(function(e){
	    $('#registerModal').modal('show');
	    $('.sign_in').removeClass('open');
    });

    $(".storage-select").select2({
	    minimumResultsForSearch: -1,
	    allowClear: true
    });

// Generic select2
    SbModel.SetUpSelect2();

    $("#country, #accounttype, #country-reg, #banklocator, #natinality, #acc-currency ").select2({  
	    minimumResultsForSearch: -1,
    });
    $(document).on('change', '.btn-file :file', function() {
	    var input = $(this),
		    numFiles = input.get(0).files ? input.get(0).files.length : 1,
		    label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
	    input.trigger('fileselect', [numFiles, label]);
    });
		
    $(document).ready( function() {
	    $('.btn-file :file').on('fileselect', function(event, numFiles, label) {
				
		    var input = $(this).parents('.input-group').find(':text'),
			    log = numFiles > 1 ? numFiles + ' files selected' : label;
				
		    if( input.length ) {
			    //input.val(log);
		    } else {
			    //if( log ) alert(log);
		    }
				
	    });
	    $('.input-group.date').datepicker({
		    format: "dd/mm/yy",
		    todayHighlight: true
	    });
    });
		
// Login

    $("#header-signin").on("shown.bs.dropdown", function () {
        $("#inputEmail3").focus();
    });
    

// input-number, btn-number

    $(document).on("click", ".btn-number", function(e) {
        e.preventDefault();

        var type = $(this).attr('data-type');
        var input = $(this).closest(".input-group").find(".input-number");
        var currentVal = parseInt(input.val());
        var step = parseInt(input.attr("step")) || 1;

        // Adjust currentVal to be a multiple of the step
        currentVal = currentVal - (currentVal % step);

        if (!isNaN(currentVal)) {
            if (type == 'minus') {
                var rawMin = input.attr('min');
                if (typeof rawMin == "undefined" || currentVal > rawMin) {
                    input.val(currentVal - step).change();
                }
                if (parseInt(input.val()) == rawMin) {
                    $(this).attr('disabled', true);
                }
            } else if (type == 'plus') {
                var rawMax = input.attr('max');
                if (typeof rawMax == "undefined" || currentVal < rawMax) {
                    input.val(currentVal + step).change();
                }
                if (parseInt(input.val()) == rawMax) {
                    $(this).attr('disabled', true);
                }
            }
        } else {
            input.val(0);
        }
    });

    $(document).on("focusin", ".input-number", function (e) {
        $(this).data('oldValue', $(this).val());
    });

    $(document).on("change", ".input-number", function (e) {
        var rawMinValue = $(this).attr("min");
        var rawMaxValue = $(this).attr("max");
        var stepValue = $(this).attr("step") || 1.0;
        var minValue = parseFloat(rawMinValue);
        var maxValue = parseFloat(rawMaxValue);
        var valueCurrent = parseFloat($(this).val());
        if (isNaN(valueCurrent)) {
            // reset the value of the box back to 0
            valueCurrent = 0;
            $(this).val(0);
            $(this).change();
            return;
        }

        // Step check
        // would have been better to use modulo but it doesn't work
        // so convert all of the numbers to integer before doing work
        var stepPower = Math.round(Math.log10(stepValue)*-1);
        var valueCurrentPowered = valueCurrent*Math.pow(10, stepPower);
        if (valueCurrentPowered !== Math.round(valueCurrentPowered)) {
            var valueToWrite = valueCurrent.toFixed(stepPower);
            $(this).val(valueToWrite);
            $(this).change();
            return;
        }

        // Minimum check
        if (typeof rawMinValue == "undefined" || valueCurrent >= minValue) {
            $(this).closest(".input-group").find(".btn-number[data-type='minus']").removeAttr('disabled');
        } else if (!isNaN(minValue) && valueCurrent < minValue) {
            alert('Sorry, the minimum value was reached');
            $(this).val(minValue);
            $(this).change();
            return;
        } else {
            $(this).val(0);
            return;
        }

        // Maximum check
        if (typeof rawMaxValue == "undefined" || valueCurrent <= maxValue) {
            $(this).closest(".input-group").find(".btn-number[data-type='plus']").removeAttr('disabled');
        } else if (!isNaN(maxValue) && valueCurrent > maxValue) {
            alert('Sorry, the maximum value was reached');
            $(this).val(maxValue);
            $(this).change();
            return;
        } else {
            $(this).val(0);
            return;
        }
    });

    $(document).on("keydown", ".input-number", function (e) {
        // Allow: backspace, delete, tab, escape, enter and .
        if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 190]) !== -1 ||
            // Allow: Ctrl+A
            (e.keyCode == 65 && e.ctrlKey === true) ||
            // Allow: home, end, left, right
            (e.keyCode >= 35 && e.keyCode <= 39)) {
            // let it happen, don't do anything
            return;
        }
        // Ensure that it is a number and stop the keypress
        if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
            e.preventDefault();
        }
    });

    // CKEditor
    var ckEditorFocusHandle = null;
    if (typeof CKEDITOR === "object") {
        // CKEditor
        $(".ckeditor").each(function(index, element) {
            CKEDITOR.replace(element.id);
        });
        
        // Find all CKEditor objects, and then set it so then when either one of them are focused on,
        // we implement a refresh every 30 seconds.
        for (let i in CKEDITOR.instances) {
            CKEDITOR.instances[i].on("focus", function() {
                if (ckEditorFocusHandle) return false;
                ckEditorFocusHandle = window.setInterval(SbModel.ST.CheckAndRefreshSession, 30000);
            });
        }
    }
    $(document).on("click", "#session-timeout-extend", function() {
        SbModel.ST.CheckAndRefreshSession(true);
    });

// Handler of nested forms, in case the browser ignores

    $(document).on("click", "form form > button[type='submit'], form form > input[type='submit']", function(event) {
        var $btn = $(event.target);
        $btn.closest("form").submit();
    });

// Button that confirms submission, and disables when the customer confirms

    $(document).on("click",
        "a.btn-confirm-and-disable, button.btn-confirm-and-disable, input[type='submit'].btn-confirm-and-disable",
        function(e) {
            var $target = $(e.target);

            if ($target.attr("disabled") || !confirm("Click OK to confirm your submission.")) {
                e.preventDefault();
            } else {
                $target.attr("disabled", "disabled");
                if ($target.is("input[type='submit']")) {
                    $target.val("Submission in progress...");
                } else {
                    $target.text("Submission in progress...");
                }
            }
        });

// Button that confirms deletion, and disables when the customer confirms

    $(document).on("click",
        "a.btn-confirm-deletion-and-disable, button.btn-confirm-deletion-and-disable, input[type='submit'].btn-confirm-deletion-and-disable",
        function (e) {
            let $target = $(e.target);

            let confirmMsg = "Click OK to continue deleting.";
            let targetDeletionType = $target.data("item-type");
            if (targetDeletionType) {
                confirmMsg = `Are you sure you would like to delete this ${targetDeletionType}? ${confirmMsg}`;
            }

            if ($target.attr("disabled") || !confirm(confirmMsg)) {
                e.preventDefault();
            } else {
                $target.addClass("disabled"); // don't add disabled attribute; it prevents submission in Chrome/Edge
                if ($target.is("input[type='submit']")) {
                    $target.val("Deletion in progress...");
                } else {
                    $target.text("Deletion in progress...");
                }
            }
            return;
        });

// Clipboard button
/*
Expected HTML:
<button type="button" class="copy-to-clipboard" data-copy="@Model.CryptoTxn.WalletAddress">
    <span class="fa fa-clipboard"></span>
</button>
*/
    $(document).on("click",
        "button.copy-to-clipboard",
        async function (e) {
            // Find the button
            let target = $(e.target);
            if (target.is("span")) {
                target = target.parent();
            }
            
            // Get the data to copy
            let dataToCopy = target.data("copy");
            try {
                // Do the actual copy
                await navigator.clipboard.writeText(dataToCopy);
                
                // Replace the clipboard icon with a checkbox
                let span = target.children("span");
                span.removeClass("fa-clipboard").addClass("fa-check");

                // Add an event 1 second later to put back the clipboard icon
                window.setTimeout(function () {
                    span.removeClass("fa-check").addClass("fa-clipboard");
                }, 1000);
            }
            catch (err) {
                console.log("Couldn't copy: " + err);
            }
        });

// Button that toggles a textbox's type (between "text" and "password")
/*
 * Expected HTML:
 * <button type="button toggle-textbox-type" class="btn btn-default" data-target="#txt-existing-token">
    <span class="glyphicon glyphicon-eye-open"></span>
</button>
 */
    $(document).on("click",
        "button.toggle-textbox-type",
        function (e) {
            // Find the button
            let button = $(e.target);
            if (button.is("span")) {
                button = button.parent();
            }

            // Get the textbox to toggle
            let textBoxSelector = button.data("target");
            let textBox = $(textBoxSelector);
            if (textBox.attr("type") === "password") {
                textBox.attr("type", "text");
                // Toggle the button's icon to the next action
                button.children("span").removeClass("glyphicon-eye-open").addClass("glyphicon-eye-close")
            } else {
                textBox.attr("type", "password");
                // Toggle the button's icon to the next action
                button.children("span").removeClass("glyphicon-eye-close").addClass("glyphicon-eye-open")
            }
        });

// Site notices
    window.setTimeout(function(){
        $(".sitenotice-container-outer").collapse("show");
    }, 750);

    // Consume all the functions in _sbJsFuncsAfterLoading
    if (SbModel && SbModel.ConsumeJsFunctionsAfterLoading) {
        //$('#ko-support-container').load('/Widgets/KoSupport',
        //    function() {
        //        SbModel.ConsumeJsFunctionsAfterLoading();
        //    });

        SbModel.ConsumeJsFunctionsAfterLoading();
    }

    $.ajax({
        url: "/Account/CheckIfShouldDormantPopup?rand=" + Math.random(),
        type: "Get",
       
    }).done(function (response) {
        if (response.popup == true) {
            $('#dormant-popup-anchor').trigger('click');
        }
    }).always(function () {
        
    });

// Cloudflare Turnstile on login
// Forms should be tagged with class="login" and should have a child div classed "cloudflare-turnstile"
// e.g. <form class="login">
// <div class="cloudflare-turnstile"></div>
// </form>
    $(document).on("submit",
        "form.login-form",
        function (e) {
            // Perform the intercept only if the CAPTCHA field is not filled in
            let captchaTokenInput = e.target.querySelector("input[name='CaptchaToken']");
            if (captchaTokenInput.dataset.hasToken == true || captchaTokenInput.dataset.hasToken == "true") {
                return true;
            }

            let tsElement = e.target.querySelector("div.cloudflare-turnstile");
            tsElement.parentElement.classList.remove("hidden");

            let tsWidgetId =
                turnstile.render(tsElement, {
                    sitekey: window.captchaSiteKey,
                    callback: function (captchaToken) {
                        captchaTokenInput.value = captchaToken; 
                        captchaTokenInput.dataset.hasToken = true;
                        turnstile.remove(tsWidgetId);
                        tsElement.parentElement.classList.add("hidden");
                        $(e.target).trigger("submit");
                    }
                });

            // Prevent submission only if the widget configured successfully
            if (tsWidgetId) {
                e.preventDefault();
            }
        });
    
        var _sessionTimeoutMins = null;

        function onActivity() {
            localStorage.setItem('lastActivityTimestamp', Date.now());
        }

        function onPolling() {
            const myPolling = setInterval(() => {
            const lastActivityTimestamp = +localStorage.getItem('lastActivityTimestamp');
            const currentTime = Date.now();
            if (_sessionTimeoutMins && (currentTime - lastActivityTimestamp) > (_sessionTimeoutMins * 60 * 1000)) {
                clearInterval(myPolling);
                logOut();
            }
            }, 1000);
        }

        function logOut() {
            localStorage.removeItem('lastActivityTimestamp');
            $.ajax({
            url: '/Account/Logout',
            type: 'GET',
            success: function (response) {
                location.href = '/Account/SessionTimeout';
            },
            error: function (error) {
                // Log out already called on other browser tab
                location.href = '/Account/SessionTimeout';
            }
            });
        }

        // Called in _LoginDropdownLoggedIn.cshtml line 154
        function startDetectUserActivity(sessionTimeoutMins) {
            _sessionTimeoutMins = sessionTimeoutMins;
            window.addEventListener('mousedown', onActivity);
            window.addEventListener('keydown', onActivity);
            window.addEventListener('wheel', onActivity);
            localStorage.setItem('lastActivityTimestamp', Date.now());
            onPolling();
        }

        window.startDetectUserActivity = startDetectUserActivity;
})();