(function($) {
  function onTilesLoaded(callback, timeout) {
    if ($('.tileWrapper').length > 0) {
      callback();
      return;
    }

    if (timeout > 0) {
      setTimeout(onTilesLoaded(callback, timeout - 100), timeout);
    }

    return;
  }

  function pairTiles() {
    var tiles = $('.paired-collection, .empty');
    if (tiles.length === 0) return;

    tiles.each(function() {
      var tile = $(this);

      if (
        (tile.hasClass('empty') &&
          tile.closest('.collectionTile').hasClass('tile-sx')) ||
        tile.hasClass('tile-sx')
      ) {
        tile.closest('.tileWrapper').addClass('tile-sx');
      } else if (
        (tile.hasClass('empty') &&
          tile.closest('.collectionTile').hasClass('tile-dx')) ||
        tile.hasClass('tile-dx')
      ) {
        tile.closest('.tileWrapper').addClass('tile-dx');
      }
    });
  }

  function createCollapse() {
    $('.collapse-wrapper').each(function() {
      var collapse = '';
      var header = $(this)
        .find('.collapse-header')
        .html();
      var collapseId =
        'collapse-' +
        header
          .trim()
          .replace(/[\W_]+/g, '')
          .toLowerCase();
      var content = $(this)
        .find('.collapse-content')
        .html();

      // prettier-ignore
      collapse = '<button class="btn btn-default" type="button" data-toggle="collapse" data-target="#' + collapseId + '" aria-expanded="false" aria-controls="' + collapseId + '">' +
                 '  <i class="fa fa-plus"></i>' +
                 '  <span>' + header + '</span>' +
                 '</button>' +
                 '<div class="collapse" id="' + collapseId + '">' +
                 '  <div class="collapse-content">' +
                      content +
                   '</div>' +
                 '</div>';

      $(this).html(collapse);
    });
  }

  $(document).ready(function() {
    //expand/collapse tile
    $('div.tile-advanced-static.collapsible').each(function() {
      var $tile = $(this);
      var $header = $($tile.find('h3'));
      var $body = $($tile.find('.tileBody'));
      $header.prepend(
        '<i class="expand-icon fa fa-chevron-down" aria-hidden="true"></i>'
      );
      if ($tile.hasClass('collapsed')) {
        $body.slideUp();
      }
      $header.click(function(e) {
        e.preventDefault();
        $tile.toggleClass('collapsed');
        if (!$tile.hasClass('collapsed')) {
          $body.slideDown();
          $header
            .find('i.expand-icon')
            .removeClass('fa-chevron-down')
            .addClass('fa-chevron-up');
        } else {
          $body.slideUp();
          $header
            .find('i.expand-icon')
            .removeClass('fa-chevron-up')
            .addClass('fa-chevron-down');
        }
      });
    });

    // return-to-top arrow
    $(window).scroll(function() {
      if ($(this).scrollTop() >= 50) {
        // If page is scrolled more than 50px
        $('#return-to-top').fadeIn(200); // Fade in the arrow
      } else {
        $('#return-to-top').fadeOut(200); // Else fade out the arrow
      }
    });
    $('#return-to-top').click(function() {
      // When arrow is clicked
      $('body,html').animate(
        {
          scrollTop: 0, // Scroll to top of body
        },
        500
      );
    });

    /*
    // hover on news home
    $('.boxNotizieHome .boxNewsImg .linkItem a').hover(function() {
      $(this)
        .parents('.boxNewsImg')
        .toggleClass('imgHover');
    });
    */

    $('#dropdown-lang').on('click', function(e) {
      $('ul.languages').toggleClass('open');
    });

    /*
     * mobile: search button action
     */
    $('#search-toggle').on('click', function(e) {
      $('#portal-searchbox').toggleClass('open');
      $('#search-toggle').toggleClass('open');
      $('body').toggleClass('searchOpened');

      if ($('#portal-searchbox').hasClass('open')) {
        $('#searchGadget').focus();
      }
    });

    /*
     * mobile: menu toggle click
     */
    $('button.plone-navbar-toggle').on('click', function(e) {
      $('#portal-mainnavigation').addClass('open');
      $('body').addClass('menuOpened');
    });

    $('#globalnav-close').on('click', function(e) {
      $('#portal-mainnavigation').removeClass('open');
      $('body').removeClass('menuOpened');
    });

    /*
     *  share button position
     */
    var $share = $('.share');
    if ($('#portal-column-two').length > 0) {
      $('#portal-column-two').prepend($share);
      $share.addClass('share-visible');
    }

    /*
     * share button behavior
     */
    $('.share .share-toggle').on('click', function(e) {
      e.preventDefault();
      $share.toggleClass('open');
    });

    /*
     * gestione click fuori per chiudere menu, ricerca e condividi
     */
    $(document).on('click', function(e) {
      if (
        !$(e.target).closest('#portal-searchbox').length &&
        !$(e.target).closest('button#search-toggle').length &&
        $(window).width() <= 991
      ) {
        $('#portal-searchbox').removeClass('open');
        $('#search-toggle').removeClass('open');
        $('body').removeClass('searchOpened');
      }

      if (!$(e.target).closest('.share').length) {
        $('.share').removeClass('open');
      }

      if (
        !$(e.target).closest('#portal-mainnavigation').length &&
        !$(e.target).closest('button.plone-navbar-toggle').length &&
        $(window).width() <= 991
      ) {
        $('#portal-mainnavigation').removeClass('open');
        $('body').removeClass('menuOpened');
      }

      if (!$(e.target).closest('.dropdown-languages').length) {
        $('ul.languages').removeClass('open');
      }
    });

    $('#portal-footer-wrapper').prepend($('.portlet.footer-logo'));
    $('#portal-footer-wrapper').prepend($('.portlet.valuta-sito'));

    onTilesLoaded(pairTiles);

    createCollapse();
  });
})(jQuery);
