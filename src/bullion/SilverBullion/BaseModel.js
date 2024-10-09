
(function () {

    $(document).ready(function () {
        if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
            $(".viewport-switch").removeClass("hidden");
        }
        $("#menu-toggle").click(function (e) {
            e.preventDefault();
            $("#wrapper").toggleClass("toggled");
        });
        // $("#sidebar-accordion a").click(function (e) {
        //     if ($(e.target).attr("href").indexOf("#") > 0) {
        //         $("#wrapper").toggleClass("toggled");
        //     }
        // });

        //function dontDropLogin() {
        //    if ($(window).width() < 767) {
        //        $("#header-signin-link").on("click", function () {
        //            window.location.replace($(this).attr("href"));
        //        });
        //    }
        //}
        //$(window).on("resize", dontDropLogin);
        //dontDropLogin();
    });

    // The actual SbModel object is declared in _SbJsFuncsAfterLoading.cshtml
    SbModel.ReBind = function () {
        ko.unapplyBindings($(document), true);
        ko.applyBindings(SbModel);
    };

    SbModel.UserIsAnonymous = true,
    SbModel.UserIsUser = true,

    SbModel.FixHeader = function () {
        $("header").removeClass("navbar-static-top").addClass("navbar-fixed-top");
        $("body").css("padding", "");
    },
    SbModel.UnfixHeader = function () {
        $("header").removeClass("navbar-fixed-top").addClass("navbar-static-top");
        $("body").css("padding", 0);
    },
    SbModel.SetUpSelect2 = function (select2Elements) {
        if (typeof select2Elements !== "object")
            select2Elements = $("select.select2");

        select2Elements.each(function (i, e) {
            var drp = $(e);
            if (drp.data("select2")) return;

            var select2Options = {};
            //Deprecated
            //if (drp.data("type")) {
            //    select2Options["dropdownCssClass"] = drp.data("type");
            //}
            drp.select2(select2Options);
        });
    },
    SbModel.SetUpToc = function () {

        function adjustHeights() {
            $('.sidebar_container').height($('.sidebar_container').height());
            $(document.body).trigger("sticky_kit:recalc");
            $("body").scrollspy("refresh");
        }

        function initFixSidebar() {

            if ($(window).width() > 991) {
                // Unfix the top portion of the page
                SbModel.UnfixHeader();
                $(".sidebar_left").removeClass("relative_position");

                // Scrollspy
                $("body").scrollspy({ target: ".page_toc" });

                $("dl.collapsible-list dd").on("shown.bs.collapse", adjustHeights);
                $("dl.collapsible-list dd").on("hidden.bs.collapse", adjustHeights);
                adjustHeights();

                // Hashchange
                function openFaqHash() {
                    var $e = $(location.hash);
                    if ($e.is("dl.collapsible-list dt")) {
                        $e.next("dd").collapse("show");
                    }
                }

                $(window).on("hashchange", openFaqHash);
                if (location.hash) {
                    openFaqHash();
                }

                if ($('.sidebar_container').parent().height() < $('.storageMenu').parent().height()) {
                    $('.sidebar_container').height($('.storageMenu').parent().height());
                } else {
                    $('.sidebar_container').height($('.sidebar_container').parent().height());
                }
                $(".sidebar_left").stick_in_parent({ offset_top: 0 });
            } else {

                $("dl.collapsible-list dd").unbind();
                $("dl.collapsible-list dd").unbind();
                //$(window).unbind();

                SbModel.FixHeader();
                $('.sidebar_container').height($('.sidebar_left').height());
                $(".sidebar_left").addClass("relative_position");
            }
        }
        $(window).on("resize", initFixSidebar);
        initFixSidebar();
        function handlingSidebarSticky() {
            // calculating footer position bottom
            var footerPaddingTop = +($('.footer').css('padding-top')?.slice(0, $('.footer').css('padding-top')?.length - 2));
            var footerPositionBottom = ($('.footer').position()?.top + footerPaddingTop) - ($(window).scrollTop() + $(window).height());
            if (footerPositionBottom < 0 && $(window).width() > 992) {
                $(".sidebar_left").css({ "top": `${footerPositionBottom}px` });
            } else {
                $(".sidebar_left").css({ "top": 0 });
            }
        }
        $(window).on('scroll', handlingSidebarSticky);
        handlingSidebarSticky();
    },


    // Session timeout management
    SbModel.ST = {
        /** The last time that the customer interacted with the server (takes the LastActivity cookie) */
        _LastActivityWithServer: new Date(),
        /** Session timeout in milliseconds */
        _SessionTimeoutInMs: 1200000, // 20 minutes default (can be overridden)
        /** Session timeout warning shows up before timeout */
        _SessionTimeoutWarningInMs: 60000, // 1 minute
        /**  */
        _UpdateActivityLock: false,

        /** Handle that shows the session timeout warning */
        _SessionTimeoutWarningHnd: null,
        /** Handle that checks if the user is still logged in, and if not, redirects to the logout page */
        _SessionTimeoutHnd: null,
        /** Handle that animates the countdown */
        _TimeoutCountdownHnd: null,

        _SessionTimeoutBoxSelector: "#session-timeout-warning",
        _CountdownSelector: "#session-timeout-secs",

        CheckAndRefreshSession: function (ignoreLock) {
            if (!SbModel.ST._UserShouldHaveTimeoutActivated()) return;
            if (!ignoreLock && SbModel.ST._UpdateActivityLock) return;

            var lastUpdate = new Date() - SbModel.ST._LastActivityWithServer;
            if (lastUpdate >= 500) {
                SbModel.ST.UpdateActivityLock = true;

                $.post("/Widgets/KeepAlive", null, function () {
                    SbModel.ST._LastActivityWithServer = SbModel.ST._GetLastActivity();
                    SbModel.ST.UpdateActivityLock = false;

                    SbModel.ST.UpdateSessionTimeoutHandles();
                });
            }
        },
        UpdateSessionTimeoutHandles: function () {
            if (!SbModel.ST._UserShouldHaveTimeoutActivated()) return;

            if (SbModel.ST._SessionTimeoutWarningHnd != null) {
                window.clearTimeout(SbModel.ST._SessionTimeoutWarningHnd);
                SbModel.ST._SessionTimeoutWarningHnd = null;
            }
            if (SbModel.ST._SessionTimeoutHnd != null) {
                window.clearTimeout(SbModel.ST._SessionTimeoutHnd);
                SbModel.ST._SessionTimeoutHnd = null;
            }
            if (SbModel.ST._TimeoutCountdownHnd != null) {
                window.clearInterval(SbModel.ST._TimeoutCountdownHnd);
                SbModel.ST._SessionTimeoutWarningHnd = null;
            }

            SbModel.ST._SessionTimeoutWarningHnd =
                window.setTimeout(SbModel.ST._HandleSessionTimeoutWarning, SbModel.ST._SessionTimeoutInMs - SbModel.ST._SessionTimeoutWarningInMs);
            SbModel.ST._SessionTimeoutHnd =
                window.setTimeout(SbModel.ST._HandleSessionTimeout, SbModel.ST._SessionTimeoutInMs);
            $(SbModel.ST._SessionTimeoutBoxSelector).addClass("hidden");
        },
        _UserShouldHaveTimeoutActivated: function () {
            return (!SbModel.UserIsAnonymous && SbModel.UserIsUser);
        },
        _HandleSessionTimeoutWarning: function () {
            // Check if there's still time remaining (due to other activity)
            // If there's still ample time, postpone the handling of the timeout warning
            SbModel.ST._LastActivityWithServer = SbModel.ST._GetLastActivity();
            var timeRemainingMs = SbModel.ST._SessionTimeoutInMs - (new Date() - SbModel.ST._LastActivityWithServer);
            if (timeRemainingMs > SbModel.ST._SessionTimeoutWarningInMs) { 
                window.setTimeout(SbModel.ST._HandleSessionTimeoutWarning, timeRemainingMs - SbModel.ST._SessionTimeoutWarningInMs);
                return; 
            }

            SbModel.ST._UpdateActivityLock = false;
            SbModel.ST._TimeoutCountdownHnd =
                window.setInterval(SbModel.ST._HandleTimerUpdate, 1000);
            $(SbModel.ST._SessionTimeoutBoxSelector).removeClass("hidden");
        },
        _HandleSessionTimeout: function () {
            $.post("/Account/IsLoggedIn", null, function (isLoggedIn) {
                if (!isLoggedIn) {
                    window.location = "/Account/SessionTimeout";
                } else {
                    SbModel.ST.UpdateSessionTimeoutHandles();
                }
            }, "json");
        },
        _HandleTimerUpdate: function () {
            // Check if there's still time remaining (due to other activity)
            // If there's still ample time, postpone the handling of the timeout warning
            SbModel.ST._LastActivityWithServer = SbModel.ST._GetLastActivity();
            var timeRemainingMs = SbModel.ST._SessionTimeoutInMs - (new Date() - SbModel.ST._LastActivityWithServer);
            if (timeRemainingMs > SbModel.ST._SessionTimeoutWarningInMs) { 
                window.setTimeout(SbModel.ST._HandleSessionTimeoutWarning, timeRemainingMs - SbModel.ST._SessionTimeoutWarningInMs);
                $(SbModel.ST._SessionTimeoutBoxSelector).addClass("hidden");
                return; 
            }

            var timeRemaining = Math.round(timeRemainingMs / 1000);
            $(SbModel.ST._CountdownSelector).text(Math.max(timeRemaining, 0));

            // Adjust width
            var progress = 1 - timeRemainingMs*1.0/60000;
            $("#session-timeout-warning-progress").width(progress*100 + "%");
        },
        _GetLastActivity: function () {
            // Try to get the last activity from cookies ("LastActivity")
            var lastActivityCookie = document.cookie.match(/LastActivity=(\d+)/);
            if (lastActivityCookie && lastActivityCookie.length === 2) {
                return new Date(lastActivityCookie[1]*1000);
            }
            return new Date();
        }
    }

    /**
     * Converts a given amount of seconds as "x:xx minutes", "0:xx seconds"
     * 
     * @param {number} seconds - Number of seconds to convert
     */
    SbModel.FormatAsMinsSecs = function (seconds) {
        seconds = Math.floor(seconds);

        var secs = seconds % 60;
        var mins = (seconds-secs)/60;
            
        var periodToUse = "minutes";
        if (mins === 0) {
            periodToUse = "second";
            if (secs > 1)
                periodToUse = "seconds";
        }

        return mins + ":" + ("0"+secs).slice(-2) + " " + periodToUse;
    }

})();