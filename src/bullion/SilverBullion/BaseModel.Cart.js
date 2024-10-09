(function() {

    // This will hold the cart contents
    SbModel.Cart = {
        LocalInStock: ko.observable(),
        LocalPreOrder: ko.observable(),
        StarInStock: ko.observable(),
        StarPreOrder: ko.observable(),

        GramsInStock: ko.observable(),
        GramsPreOrder: ko.observable(),

        GMSLocalInStock: ko.observable(),
        GMSStarInStock: ko.observable(),

        GraphicParams: ko.observable(),
        CountedOzBase: ko.observable(),
        CountedOzCur: ko.observable(),
        BozToNextTierPreempt: ko.observable(),

        CountTotal: ko.observable(0),

        ErrorMessage: ko.observable(),
        ErrorSource: ko.observable(''),
        ErrorLimit: ko.observable(''),
        CanStillProceed: ko.observable(true), // computed by server-side
        PaidStorageMonths: ko.observable(6),
        OldPaidStorageMonths: 6,
        Currency: ko.observable("SGD"),
        PaymentOption: ko.observable(), // the selected payment option
        PaymentOptions: ko.observable(), // all available payment options
        BranchID: ko.observable(""),

        DiscountTierCur: ko.observable(),
        StorageChargesTotalStr: ko.observable(),

        //needed by MYSB
        DiscountTierBase: ko.observable(),
        NextBozBoundary: ko.observable(),

        Total: ko.observable(),
        TotalStr: ko.observable(),
        TotalExCcStr: ko.observable(),

        StorageChargesTotalStr: ko.observable(),

        $PreviousState: {},

        ShowBaseCur: ko.observable(false),
        ToggleShowBaseCurLabel: ko.pureComputed(function() {
            return SbModel.Cart.ShowBaseCur() ? "[- hide details]" : "[+ show details]";
        }),

        CartIsAdding: false,
        CartFieldIsUpdating:
            ko.observable(false), // flag that is set when the cart modal is calling a server-side procedure
        PaidStorageMonthsIsUpdating: false,

        LockAmountExpiryEpochUtc: ko.observable(0),
        TimeNow: ko.observable((new Date()).getTime()),
        PriceExpirySecs: ko.pureComputed(function() {
            return Math.round((SbModel.Cart.LockAmountExpiryEpochUtc() - SbModel.Cart.TimeNow()) / 1000);
        }),
        PriceExpiryDisplay: ko.pureComputed(function() {
            var expirySecs = SbModel.Cart.PriceExpirySecs();
            return SbModel.FormatAsMinsSecs(expirySecs);
        }),

        //SB-4971
        CryptoOwnedAddress: ko.observable(''),
        CryptoOwnedAddressSource: ko.observable(''),

        /** Determines if the front-end should allow the customer to go to the checkout (server-side flag CanStillProceed plus a check on the payment option and CartFieldIsUpdating) */
        CanStillProceedOnClient: ko.pureComputed(function () {
            if (SbModel.Cart.CartFieldIsUpdating()) return false;

            var paymentOpt = SbModel.Cart.PaymentOption();
            var paymentOptObj = 
                SbModel.Cart.PaymentOptions()
                    .find(function (pOpt) { return pOpt.Code() === paymentOpt });
            var paymentOptIsEnabled = paymentOptObj && paymentOptObj.IsOmitted && paymentOptObj.IsOmitted() === false;

            // Client can proceed if the option is enabled, or there's only one option allowed (in the case of crypto)
            var clientCanProceed = paymentOptIsEnabled || SbModel.Cart.PaymentOptions().length === 1;

            return SbModel.Cart.CanStillProceed() && clientCanProceed;
        }),

        _GetRequestVerificationToken: function () {
            // Prioritize the #cartModal RVF (i.e. the one inside the popup.)
            // Otherwise we take on the RVF inside the #cartKoWidget (right sidebar of products page)
            var rvf = $("#cartModal input[name='__RequestVerificationToken']");
            if (!rvf.length)
                rvf = $("#cartKoWidget input[name='__RequestVerificationToken']");
            return rvf.val();
        },

        _CreateShoppingCart: function (data) {
            var newCart = ko.mapping.fromJS(data, {
                "Items": {
                    "create": function(options) {
                        return SbModel.Cart._CreateShoppingCartItem(data.CartType, data.IsInStock, options.data);
                    },
                    key: function(data) {
                        return ko.utils.unwrapObservable(data.ProductId);
                    }
                }
            });
            newCart.RemoveItem = function (item) {
                SbModel.Cart._BeforeUpdating();

                $.ajax({
                    url: "/CartJson/Delete?rand=" + Math.random(),
                    type: "POST",
                    data: {
                        CartType: item.CartType(),
                        IsInStock: item.IsInStock(),
                        ProductId: item.ProductId(),
                        GetFullCart: true
                    },
                    headers: {
                        // Old token: $("#cartModal input[name='__RequestVerificationToken']").val()
                        __RequestVerificationToken: SbModel.Cart._GetRequestVerificationToken()
                    }
                }).done(function(response) {
                    SbModel.Cart._UpdateMe(response);
                }).fail(function(jqxhr, textStatus, error) {
                    SbModel.Cart._UpdateMeFromPrevious();
                    SbModel.Cart.ErrorMessage(error);
                }).always(function() {
                    SbModel.Cart._DoAlwaysAfterUpdating();
                });
            };
            newCart.ShowCartSidebarItem = function(el) {
                if (el.nodeType === 1) {
                    $(el).hide().slideDown();
                }
            };
            newCart.HideCartSidebarItem = function(el) {
                if (el.nodeType === 1) {
                    $(el).slideUp(function() { $(el).remove(); });
                }
            };
            newCart.HighlightCartSidebarItem = function (el) {
                if (el.nodeType === 1) {
                    $(el).css("background-color", "gold");
                }
            };
            return newCart;
        },
        _CreateShoppingCartItem: function (cartType, cartIsInStock, itemData) {
            var newItem = ko.mapping.fromJS(itemData);
            newItem.CartType = ko.observable(cartType);
            newItem.IsInStock = ko.observable(cartIsInStock);
            newItem.SavedQty = newItem.Quantity();
            newItem.selectedCount = ko.pureComputed(function () {
                return newItem.SelectableParcels().filter(function (parcel) {
                    return parcel.Selected() === true
                }).length;
            });
            newItem.IsAvgPricing = ko.pureComputed(function () {
                return newItem.SelectableParcels().length > 0 && newItem.Quantity() > 1
            })

            // Pagination
            newItem.itemsPerPage = ko.observable(20);
            newItem.currentPage = ko.observable(1);
            newItem.items = ko.observableArray([]);

            newItem.totalPages = ko.computed(function () {
                return Math.ceil(newItem.SelectableParcels().length / newItem.itemsPerPage());
            });

            newItem.pagedItems = ko.computed(function () {
                var startIndex = (newItem.currentPage() - 1) * newItem.itemsPerPage();
                return newItem.SelectableParcels().slice(startIndex, startIndex + newItem.itemsPerPage());
            });

            newItem.nextPage = function () {
                if (newItem.currentPage() < newItem.totalPages()) {
                    newItem.currentPage(newItem.currentPage() + 1);
                }
            };

            newItem.previousPage = function () {
                if (newItem.currentPage() > 1) {
                    newItem.currentPage(newItem.currentPage() - 1);
                }
            };

            newItem.goToPage = function (page) {
                if (page >= 1 && page <= newItem.totalPages()) {
                    newItem.currentPage(page);
                }
            };


            newItem.Quantity.subscribe(function (newQty) {
                if (newItem.SavedQty == newQty || SbModel.Cart.CartIsAdding) return; // detect if the quantity really changed
                newItem.SavedQty = newQty;

                var formToValidate = $("#cartModal");
                if (formToValidate.length === 0) {
                    formToValidate = $("#cartKoWidget");
                }
                formToValidate.validate({ debug: true });
                if (formToValidate.valid()) {
                    SbModel.Cart._BeforeUpdating();
                    $.ajax({
                        url: "/CartJson/Edit?rand=" + Math.random(),
                        type: "POST",
                        data: {
                            CartType: newItem.CartType(),
                            IsInStock: newItem.IsInStock(),
                            ProductId: newItem.ProductId(),
                            Qty: newQty,
                            GetFullCart: true
                        },
                        headers: {
                            __RequestVerificationToken: SbModel.Cart._GetRequestVerificationToken()
                        },
                        beforeSend: function () {
                            $(".blocked").show();
                        }
                    }).done(function(response) {
                        SbModel.Cart._UpdateMe(response);
                        $(".blocked").hide();
                    }).fail(function(jqxhr, textStatus, error) {
                        SbModel.Cart._UpdateMeFromPrevious();
                        SbModel.Cart.ErrorMessage(error);
                    }).always(function () {
                        SbModel.Cart._DoAlwaysAfterUpdating();
                    });
                }
            });

            newItem.SelectParcel = function (parcel) {
                // Check for selecting over quantity limit
                if (!parcel.Selected()) {
                    if (newItem.selectedCount() >= newItem.Quantity()) {
                        return;
                    }
                }

                parcel.Selected(!parcel.Selected()); // Toggle selection

                $.ajax({
                    url: "/CartJson/SetParcelSelection?rand=" + Math.random(),
                    type: "POST",
                    data: {
                        CartType: newItem.CartType(),
                        ProductId: newItem.ProductId(),
                        Parcels: newItem.SelectableParcels(),
                        GetFullCart: true
                    },
                    headers: {
                        __RequestVerificationToken: SbModel.Cart._GetRequestVerificationToken()
                    },
                    beforeSend: function () {
                        $(".blocked").show();
                    }
                }).done(function (response) {
                    SbModel.Cart._UpdateMe(response);
                    $(".blocked").hide();
                }).fail(function (jqxhr, textStatus, error) {
                    SbModel.Cart._UpdateMeFromPrevious();
                    SbModel.Cart.ErrorMessage(error);
                }).always(function () {
                    SbModel.Cart._DoAlwaysAfterUpdating();
                });
            };
            return newItem;
        },
        _UpdateMe: function (newData) {
            ko.mapping.fromJS(newData, koCartModelMappingOptions, SbModel.Cart);
            SbModel.Cart.$PreviousState = newData;
            SbModel.Cart._AfterUpdating();
        },
        _UpdateMeFromPrevious: function() {
            ko.mapping.fromJS(SbModel.Cart.$PreviousState, koCartModelMappingOptions, SbModel.Cart);
            SbModel.Cart._AfterUpdating();
        },
        _UpdateMeFromRemote: function (successCallback, failCallBack, alwaysCallback) {
            SbModel.Cart._BeforeUpdating();
            // Make a request to /CartJson/AsJson with a random number (this beats IE9 caching the JSON result)
            $.get("/CartJson/AsJson?rand=" + Math.random(), null, function (data) {
                    SbModel.Cart._UpdateMe(data);
                }, "json")
                .done(function() {
                    if (typeof successCallback === "function")
                        successCallback();
                })
                .fail(function() {
                    if (typeof failCallBack === "function")
                        failCallBack();
                })
                .always(function () {
                    if (typeof alwaysCallback === "function")
                        alwaysCallback();
                    SbModel.Cart._DoAlwaysAfterUpdating();
                });
        },
        _BeforeUpdating: function() {
            //$("#cartModal .progress-140px-parent").show();
            SbModel.Cart.CartFieldIsUpdating(true);
            SbModel.Cart.PaidStorageMonthsIsUpdating = true;
        },
        _AfterUpdating: function () {
            // Timeout update
            SbModel.ST.UpdateSessionTimeoutHandles();

            // Only do the following if we are actually showing the cart popup
            if ($("#cartModal").length) {
                $("#cartModal").removeData("validator").removeData("unobtrusiveValidation");
                $.validator.unobtrusive.parse("#cartModal");
            }
        },
        _DoAlwaysAfterUpdating: function() {
            SbModel.Cart.CartFieldIsUpdating(false);
            SbModel.Cart.PaidStorageMonthsIsUpdating = false;
        },
        _ToggleShowBaseCur: function () {
            SbModel.Cart.ShowBaseCur(!SbModel.Cart.ShowBaseCur());
        },
        _DisablePaymentOption: function (option, item) {
            if (item) {
                // Disables a payment option
                ko.applyBindingsToNode(option, {disable: item.IsOmitted}, item);
            }
        }
       

    };

    //identify error source if pertaining to NewAml or OverrideCrDailyLimit
    //SbModel.Cart.ErrorSource.subscribe(function (newVal) {

    //    if ((newVal === 'NewAmlDefaultLimit' ||
    //            newVal === 'OverrideCrDailyLimit') &&
    //        (SbModel.Cart.Currency() === 'BTC' ||
    //            SbModel.Cart.Currency() === 'ETH' ||
    //            SbModel.Cart.Currency() === 'CGT')
    //    )
    //        $('#limit-message-cart').removeClass("hidden");
    //    else {
    //        $('#limit-message-cart').addClass("hidden");
    //    }

    //});
    SbModel.Cart.PaidStorageMonths.subscribe(function (newVal) {
        // Only update while the popup is shown
        if (!$("#cartModal").length) return;
        // And make sure the flag is not set, and the value actually changed
        if (SbModel.Cart.PaidStorageMonthsIsUpdating ||
            SbModel.Cart.OldPaidStorageMonths == newVal) return;

        SbModel.Cart.OldPaidStorageMonths = newVal;
        SbModel.Cart.PaidStorageMonthsIsUpdating = true;
        $.ajax({
            url: "/CartJson/SetPaidStorageMonths?rand=" + Math.random(),
            type: "POST",
            data: {
                PaidStorageMonths: newVal,
                GetFullCart: true
            },
            headers: {
                __RequestVerificationToken: SbModel.Cart._GetRequestVerificationToken()
            }
        }).done(function (response) {
            SbModel.Cart._UpdateMe(response);
        }).fail(function (jqxhr, textStatus, error) {
            SbModel.Cart._UpdateMeFromPrevious();
            SbModel.Cart.ErrorMessage(error);
        }).always(function() {
            SbModel.Cart.PaidStorageMonthsIsUpdating = false;
        });
    });

    SbModel.Cart.Currency.subscribe(function (newVal) {
        // Only update while the popup is shown
        if (!$("#cartModal").length) return;
        // And make sure the flag is not set
        if (SbModel.Cart.CartFieldIsUpdating()) return;

        SbModel.Cart.CartFieldIsUpdating(true);
        $.ajax({
            url: "/CartJson/SetCartCurrency/" + newVal + "?rand=" + Math.random(),
            type: "GET",
            headers: {
                __RequestVerificationToken: SbModel.Cart._GetRequestVerificationToken()
            }
        }).done(function (response) {
            SbModel.Cart._UpdateMe(response);
        }).fail(function (jqxhr, textStatus, error) {
            SbModel.Cart._UpdateMeFromPrevious();
            SbModel.Cart.ErrorMessage(error);
        }).always(function () {
            SbModel.Cart.CartFieldIsUpdating(false);
        });
    });

    SbModel.Cart.BranchID.subscribe(function(newVal) {
        // Only update while the popup is shown
        if (!$("#cartModal").length) return;
        // And make sure the flag is not set
        if (SbModel.Cart.CartFieldIsUpdating()) return;

        SbModel.Cart.CartFieldIsUpdating(true);
        $.ajax({
            url: "/CartJson/SetBranchId/" + newVal + "?rand=" + Math.random(),
            type: "GET",
            headers: {
                __RequestVerificationToken: SbModel.Cart._GetRequestVerificationToken()
            }
        }).done(function (response) {
            SbModel.Cart._UpdateMe(response);
        }).fail(function (jqxhr, textStatus, error) {
            SbModel.Cart._UpdateMeFromPrevious();
            SbModel.Cart.ErrorMessage(error);
        }).always(function () {
            SbModel.Cart.CartFieldIsUpdating(false);
        });
    });


    SbModel.Cart.CryptoOwnedAddress.subscribe(function (newVal) {
        if (newVal === false) {
            SbModel.Cart.CryptoOwnedAddressSource('');
        }
    });

    var oneCartMapOpt = {
        "create": function (options) {
             return SbModel.Cart._CreateShoppingCart(options.data);
        },
        key: function(data) {
            return ko.utils.unwrapObservable(data.CartType) +
                   ko.utils.unwrapObservable(data.IsInStock);
        }
    };
    var koCartModelMappingOptions = {
        // For each of the carts
        "LocalInStock": oneCartMapOpt,
        "StarInStock": oneCartMapOpt,
        "LocalPreOrder": oneCartMapOpt,
        "StarPreOrder": oneCartMapOpt,
        "GramsInStock": oneCartMapOpt,
        "GramsPreOrder": oneCartMapOpt,

        "GMSLocalInStock": oneCartMapOpt,
        "GMSStarInStock": oneCartMapOpt
    };
    var koCartValidationOptions = {};

    SbModel.AddJsFunctionToRunAfterLoading(function () {
        // Prepopulate the cart object with the structure of an empty cart.
        // (#hdnEmptyCart exists in _KoInitializeValues.cshtml)
        //SbModel.Cart._UpdateMe($.parseJSON($("#hdnEmptyCart").val()));

        SbModel.Cart._UpdateMeFromRemote();

        // Set timeout to update SbModel.Cart.TimeNow
        window.setInterval(function () {
            var timeNow = (new Date()).getTime();
            SbModel.Cart.TimeNow(timeNow);
        }, 1000);

        // Add listener to prevent ENTER/RETURN from submitting the #cartModal form back to the address of the client
        $(document).on("keydown", "#cartModal", function(event) {
            if (event.which == 13) { // 13 = code for <ENTER> key
                event.preventDefault();
            }
        });
    });

})();