(function( $, undefined ) {
	//special click handling to make widget work remove after nav changes in 1.4
	var href,
		ele = "";
	$( document ).on( "click", "a", function( e ) {
		href = $( this ).attr( "href" );
		var hash = $.mobile.path.parseUrl( href );
		if( typeof href !== "undefined" && hash !== "" && href !== href.replace( hash,"" ) && hash.search( "/" ) !== -1 ){
			//remove the hash from the link to allow normal loading of the page.
			var newHref = href.replace( hash,"" );
			$( this ).attr( "href", newHref );
		}
		ele = $( this );
	});
	$( document ).on( "pagebeforechange", function( e, f ){
			f.originalHref = href;
	});
	$( document ).on("pagebeforechange", function( e,f ){
		var hash = $.mobile.path.parseUrl(f.toPage).hash,
			hashEl, hashElInPage;

		try {
			hashEl = $( hash );
		} catch( e ) {
			hashEl = $();
		}

		try {
			hashElInPage = $( ".ui-page-active " + hash );
		} catch( e ) {
			hashElInPage = $();
		}

		if( typeof hash !== "undefined" &&
			hash.search( "/" ) === -1 &&
			hash !== "" &&
			hashEl.length > 0 &&
			!hashEl.hasClass( "ui-page" ) &&
			!hashEl.hasClass( "ui-popup" ) &&
			hashEl.data('role') !== "page" &&
			!hashElInPage.hasClass( "ui-panel" ) &&
			!hashElInPage.hasClass( "ui-popup" ) ) {
			//scroll to the id
			var pos = hashEl.offset().top;
			$.mobile.silentScroll( pos );
			$.mobile.navigate( hash, '', true );
		} else if( typeof f.toPage !== "object" &&
			hash !== "" &&
			$.mobile.path.parseUrl( href ).hash !== "" &&
			!hashEl.hasClass( "ui-page" ) && hashEl.attr('data-role') !== "page" &&
			!hashElInPage.hasClass( "ui-panel" ) &&
			!hashElInPage.hasClass( "ui-popup" ) ) {
			$( ele ).attr( "href", href );
			$.mobile.document.one( "pagechange", function() {
				if( typeof hash !== "undefined" &&
					hash.search( "/" ) === -1 &&
					hash !== "" &&
					hashEl.length > 0 &&
					hashElInPage.length > 0 &&
					!hashEl.hasClass( "ui-page" ) &&
					hashEl.data('role') !== "page" &&
					!hashElInPage.hasClass( "ui-panel" ) &&
					!hashElInPage.hasClass( "ui-popup" ) ) {
					hash = $.mobile.path.parseUrl( href ).hash;
					var pos = hashElInPage.offset().top;
					$.mobile.silentScroll( pos );
				}
			} );
		}
	});
	$( document ).on( "mobileinit", function(){
		hash = window.location.hash;
		$.mobile.document.one( "pageshow", function(){
			var hashEl, hashElInPage;

			try {
				hashEl = $( hash );
			} catch( e ) {
				hashEl = $();
			}

			try {
				hashElInPage = $( ".ui-page-active " + hash );
			} catch( e ) {
				hashElInPage = $();
			}

			if( hash !== "" &&
				hashEl.length > 0 &&
				hashElInPage.length > 0 &&
				hashEl.attr('data-role') !== "page" &&
				!hashEl.hasClass( "ui-page" ) &&
				!hashElInPage.hasClass( "ui-panel" ) &&
				!hashElInPage.hasClass( "ui-popup" ) &&
				!hashEl.is( "body" ) ){
				var pos = hashElInPage.offset().top;
				setTimeout( function(){
					$.mobile.silentScroll( pos );
				}, 100 );
			}
		});
	});
})( jQuery );

// Turn off Ajax for local file browsing
if ( location.protocol.substr(0,4)  === 'file' ||
     location.protocol.substr(0,11) === '*-extension' ||
     location.protocol.substr(0,6)  === 'widget' ) {

	// Start with links with only the trailing slash and that aren't external links
	var fixLinks = function() {
		$( "a[href$='/'], a[href='.'], a[href='..']" ).not( "[rel='external']" ).each( function() {
			if( !$( this ).attr( "href" ).match("http") ){
				this.href = $( this ).attr( "href" ).replace( /\/$/, "" ) + "/index.html";
			}
		});
	};

	// Fix the links for the initial page
	$( fixLinks );

	// Fix the links for subsequent ajax page loads
	$( document ).on( "pagecreate", fixLinks );

	// Check to see if ajax can be used. This does a quick ajax request and blocks the page until its done
	$.ajax({
		url: '.',
		async: false,
		isLocal: true
	}).error(function() {
		// Ajax doesn't work so turn it off
		$( document ).on( "mobileinit", function() {
			$.mobile.ajaxEnabled = false;

			var message = $( '<div>' , {
				'class': "jqm-content",
				style: "border:none; padding: 10px 15px; overflow: auto;",
				'data-ajax-warning': true
			});

			message
			.append( "<h3>Note: Navigation may not work if viewed locally</h3>" )
			.append( "<p>The Ajax-based navigation used throughout the jQuery Mobile docs may need to be viewed on a web server to work in certain browsers. If you see an error message when you click a link, please try a different browser.</p>" );

			$( document ).on( "pagecreate", function( event ) {
				$( event.target ).append( message );
			});
		});
	});
}

$( document ).on( "pagecreate", ".bdoty", function( event ) {
	var search,
		page = $( this ),
		that = this

	// Global navmenu panel
	$( ".bdoty-navmenu ul" ).listview();

	$( ".bdoty-navmenu-link" ).on( "click", function() {
		page.find( ".bdoty-navmenu:not(.jqm-panel-page-nav)" ).panel( "open" );
	});

	$( ".bdoty-hymn-menu" ).click( function(event) {
		selected = $( event.target ).attr('data-hymn'); 
		$( "#hymnmenu" ).find( ".bdoty-hymn-edit" ).attr("href", "/hymns/edit?k=" + selected); 
		$( "#hymnmenu" ).find( ".bdoty-hymn-delete" ).attr("href", "/hymns/delete?k=" + selected);
	});




	// Fix links on homepage to point to sub directories
	if ( $( event.target ).hasClass( "jqm-home") ) {
		$( this ).find( "a" ).each( function() {
			$( this ).attr( "href", $( this ).attr( "href" ).replace( "../", "" ) );
		});
	}
});

// Append keywords list to each list item
$( document ).one( "pagecreate", ".bdoty", function( event ) {
	$( this ).find( ".jqm-search-results-list li, .jqm-search li" ).each(function() {
		var text = $( this ).attr( "data-filtertext" );

		$( this )
			.find( "a" )
			.append( "<span class='jqm-search-results-keywords ui-li-desc'>" + text + "</span>" );
	});
});


// Extension to listview to add keyboard navigation
$( document ).on( "mobileinit", function() {
	(function( $, undefined ) {

	$.widget( "mobile.listview", $.mobile.listview, {
		options: {
			arrowKeyNav: false,
			enterToNav: false,
			highlight: false,
			submitTo: false
		},
		_create: function() {
			this._super();

			if ( this.options.arrowKeyNav ) {
				this._on( document, { "pageshow": "arrowKeyNav" });
			}

			if ( this.options.enterToNav ) {
				this._on( document, { "pageshow": "enterToNav" });
			}

		},
		submitTo: function() {
			var url,
				form = this.element.parent().find( "form" );

			form.attr( "method", "get" )
				.attr( "action", this.options.submitTo );

			url = this.options.submitTo + "?search=" + this.element.parent().find( "input" ).val();

			window.location =  url;
		},
		enterToNav: function() {
			var form = this.element.parent().find( "form" );

			form.append( "<button type='submit' data-icon='carat-r' data-inline='true' class='ui-hidden-accessible' data-iconpos='notext'>Submit</button>" )
				.parent()
				.trigger( "create" );

			this.element.parent().find( "form" ).children( ".ui-btn" ).addClass( "ui-hidden-accessible" );

			this._on( form, {
				"submit": "submitHandler"
			});
		},
		enhanced: false,
		arrowKeyNav: function() {
			var input = this.element.prev("form").find( "input" );

			if ( !this.enhanced ) {
				this._on( input, {
					"keyup": "handleKeyUp"
				});

				this.enhanced = true;
			}
		},
		handleKeyUp: function( e ) {
			var search,
				input = this.element.prev("form").find( "input" );

			if ( e.which === $.ui.keyCode.DOWN ) {
				if ( this.element.find( "li.ui-btn-active" ).length === 0 ) {
					this.element.find( "li:first" ).toggleClass( "ui-btn-active" ).find("a").toggleClass( "ui-btn-active" );
				} else {
					this.element.find( "li.ui-btn-active a" ).toggleClass( "ui-btn-active");
					this.element.find( "li.ui-btn-active" ).toggleClass( "ui-btn-active" ).next().toggleClass( "ui-btn-active" ).find("a").toggleClass( "ui-btn-active" );
				}

				this.highlightDown();
			} else if ( e.which === $.ui.keyCode.UP ) {
				if ( this.element.find( "li.ui-btn-active" ).length !== 0 ) {
					this.element.find( "li.ui-btn-active a" ).toggleClass( "ui-btn-active");
					this.element.find( "li.ui-btn-active" ).toggleClass( "ui-btn-active" ).prev().toggleClass( "ui-btn-active" ).find("a").toggleClass( "ui-btn-active" );
				} else {
					this.element.find( "li:last" ).toggleClass( "ui-btn-active" ).find("a").toggleClass( "ui-btn-active" );
				}
				this.highlightUp();
			} else if ( typeof e.which !== "undefined" ) {
				this.element.find( "li.ui-btn-active" ).removeClass( "ui-btn-active" );

				if ( this.options.highlight ) {
					search = input.val();

					this.element.find( "li" ).each(function() {
						$( this ).removeHighlight();
						$( this ).highlight( search );
					});
				}
			}
		},
		submitHandler: function() {
			if ( this.element.find( "li.ui-btn-active" ).length !== 0 ) {
				var href = this.element.find( "li.ui-btn-active a" ).attr( "href" );

				$( ":mobile-pagecontainer" ).pagecontainer( "change", href );
				return false;
			}

			if ( this.options.submitTo ) {
				this.submitTo();
			}
		},
		highlightDown: function() {
			if ( this.element.find( "li.ui-btn-active" ).hasClass( "ui-screen-hidden" ) ) {
				this.element.find( "li.ui-btn-active" ).find("a").toggleClass( "ui-btn-active" );
				this.element.find( "li.ui-btn-active" ).toggleClass( "ui-btn-active" ).next().toggleClass( "ui-btn-active" ).find("a").toggleClass( "ui-btn-active" );
				this.highlightDown();
			}
			return;
		},
		highlightUp: function() {
			if ( this.element.find( "li.ui-btn-active" ).hasClass( "ui-screen-hidden" ) ) {
				this.element.find( "li.ui-btn-active" ).find("a").toggleClass( "ui-btn-active" );
				this.element.find( "li.ui-btn-active" ).toggleClass( "ui-btn-active" ).prev().toggleClass( "ui-btn-active" ).find("a").toggleClass( "ui-btn-active" );
				this.highlightUp();
			}
			return;
		}
	});
})( jQuery );

});

/*! Copyright (c) 2011 Brandon Aaron (http://brandonaaron.net)
 * Licensed under the MIT License (LICENSE.txt).
 *
 * Thanks to: http://adomas.org/javascript-mouse-wheel/ for some pointers.
 * Thanks to: Mathias Bank(http://www.mathias-bank.de) for a scope bug fix.
 * Thanks to: Seamus Leahy for adding deltaX and deltaY
 *
 * Version: 3.0.6
 *
 * Requires: 1.2.2+
 */

(function($) {
	var types = ['DOMMouseScroll', 'mousewheel'];

	if ($.event.fixHooks) {
		for ( var i=types.length; i; ) {
			$.event.fixHooks[ types[--i] ] = $.event.mouseHooks;
		}
	}
	$.event.special.mousewheel = {
		setup: function() {
			if ( this.addEventListener ) {
				for ( var i=types.length; i; ) {
					this.addEventListener( types[--i], handler, false );
				}
			} else {
				this.onmousewheel = handler;
			}
		},
		teardown: function() {
			if ( this.removeEventListener ) {
				for ( var i=types.length; i; ) {
					this.removeEventListener( types[--i], handler, false );
				}
			} else {
				this.onmousewheel = null;
			}
		}
	};
	$.fn.extend({
		mousewheel: function(fn) {
			return fn ? this.bind("mousewheel", fn) : this.trigger("mousewheel");
		},

		unmousewheel: function(fn) {
			return this.unbind("mousewheel", fn);
		}
	});
	function handler(event) {
		var orgEvent = event || window.event, args = [].slice.call( arguments, 1 ), delta = 0, returnValue = true, deltaX = 0, deltaY = 0;
		event = $.event.fix(orgEvent);
		event.type = "mousewheel";

		// Old school scrollwheel delta
		if ( orgEvent.wheelDelta ) { delta = orgEvent.wheelDelta/120; }
		if ( orgEvent.detail     ) { delta = -orgEvent.detail/3; }
		// New school multidimensional scroll (touchpads) deltas
		deltaY = delta;
		// Gecko
		if ( orgEvent.axis !== undefined && orgEvent.axis === orgEvent.HORIZONTAL_AXIS ) {
			deltaY = 0;
			deltaX = -1*delta;
		}
		// Webkit
		if ( orgEvent.wheelDeltaY !== undefined ) { deltaY = orgEvent.wheelDeltaY/120; }
		if ( orgEvent.wheelDeltaX !== undefined ) { deltaX = -1*orgEvent.wheelDeltaX/120; }
		// Add event and delta to the front of the arguments
		args.unshift(event, delta, deltaX, deltaY);

		return ($.event.dispatch || $.event.handle).apply(this, args);
	}
})(jQuery);
