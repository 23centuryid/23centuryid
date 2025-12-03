// ===========================================
// メインJS 
// ===========================================
jQuery(document).ready(function($) {
  let lastWindowWidth = window.innerWidth;

  function checkScroll() {
    if (window.location.pathname === "/") { // トップページのみヘッダーのクラス変更
      if ($(window).scrollTop() > 0) {
        $(".l-header").addClass("js-scroll");
      } else {
        $(".l-header").removeClass("js-scroll");
      }
    }

    if ($(window).scrollTop() > 100) {
      $(".l-pagetop").fadeIn();
    } else {
      $(".l-pagetop").fadeOut();
    }
  }

  checkScroll();
  $(window).on("scroll", checkScroll);

  $(".l-pagetop").click(function(e) {
    e.preventDefault();
    $("html, body").animate({
      scrollTop: 0
    }, 500, "swing");
  });

  // スマホメニュー内のページ内リンクをクリック時にオーバーレイメニューを閉じる
  $(".l-gNav a[href^='#']").click(function(e) {
    let target = $(this.hash);
    if (target.length) {
      e.preventDefault();

      // スマホサイズ(1024px以下)のときのみメニューを閉じる
      if (window.innerWidth <= 1024) {
        $(".l-gNav").fadeOut(300, function() {
          $("body").removeClass("js-overlay-active");
          $(".hamburger").removeClass("js-active");
        });
      }

      // スムーススクロールを実行
      let headerHeight = $(".l-header").outerHeight();
      let position = target.offset().top - headerHeight;
      $("html, body").animate({
        scrollTop: position
      }, 500, "swing");
    }
  });

  // 記事中のアンカーリンクにスムーススクロールを適用（メニュー外）
  $("a[href^='#']").not(".l-gNav a").click(function(e) {
    let target = $(this.hash);
    if (target.length) {
      e.preventDefault();
      let headerHeight = $(".l-header").outerHeight();
      let position = target.offset().top - headerHeight;
      $("html, body").animate({
        scrollTop: position
      }, 500, "swing");
    }
  });
  
  // マウスオンでサブメニュー表示（PC）
  function setupDesktopMenu() {
    $(".has-submenu").hover(
      function() {
        if (window.innerWidth > 1024) {
          $(this).find(".submenu").stop().fadeIn(200);
        }
      },
      function() {
        if (window.innerWidth > 1024) {
          $(this).find(".submenu").stop().fadeOut(200);
        }
      }
    );
  }

  setupDesktopMenu();

  // ハンバーガーメニュー
  $(".hamburger").click(function(e) {
    e.preventDefault();
    e.stopPropagation(); // 他のクリックイベントと干渉しないようにする
    $(this).toggleClass("js-active");
    $(".l-gNav").fadeToggle(300);
    $("body").toggleClass("js-overlay-active");
  });

  function closeMobileMenu() {
    console.log("メニューを閉じる処理実行"); // デバッグ用
    $(".l-gNav").fadeOut(300);
    $("body").removeClass("js-overlay-active");
    $(".hamburger").removeClass("js-active");
  }

  $(document).on("click", ".menu-arrow", function(e) {
    e.preventDefault();
    e.stopPropagation();
    let parentItem = $(this).closest(".has-submenu");
    let submenu = parentItem.find(".submenu").first();
    if (submenu.is(":visible")) {
      submenu.stop().slideUp(300);
      parentItem.removeClass("open");
    } else {
      submenu.stop().slideDown(300);
      parentItem.addClass("open");
    }
  });

  $(window).resize(function() {
    let windowWidth = window.innerWidth;

    if (Math.abs(windowWidth - lastWindowWidth) < 10) return;

    if (windowWidth >= 1025 && lastWindowWidth < 1025) {
      $(".l-gNav").fadeIn(200);
      $(".submenu").hide();
      $(".has-submenu").removeClass("open");
      $("body").removeClass("js-overlay-active");
      $(".hamburger").removeClass("js-active");
    } else if (windowWidth <= 1024 && lastWindowWidth > 1024) {
      $(".l-gNav").hide();
      $(".submenu").hide();
      $(".has-submenu").removeClass("open");
    }

    lastWindowWidth = windowWidth;
  });

});
  
// ===========================================
// YouTube & 画像モーダルウィンドウ
// ===========================================
jQuery(document).ready(function ($) {
    // **YouTubeモーダルの作成**
    let youtubeModal = document.createElement("div");
    youtubeModal.id = "youtubeModal";
    youtubeModal.className = "modal-overlay";
    youtubeModal.style.display = "none";
    youtubeModal.innerHTML = `
        <div class="modal-content">
            <span class="close-modal"></span>
            <div class="modal-body">
                <iframe id="youtubeFrame" width="560" height="315" frameborder="0" allowfullscreen></iframe>
            </div>
        </div>
    `;
    document.body.appendChild(youtubeModal);

    // **画像モーダルの作成**
    let imageModal = document.createElement("div");
    imageModal.id = "imageModal";
    imageModal.className = "modal-overlay";
    imageModal.style.display = "none";
    imageModal.innerHTML = `
        <div class="modal-content">
            <span class="close-modal"></span>
            <div class="modal-body">
                <img id="imageFrame" src="" alt="Image Preview" style="max-width:100%; height:auto;">
            </div>
        </div>
    `;
    document.body.appendChild(imageModal);

    // **YouTubeモーダルを開く**
    $(document).on("click", ".youtube-modal-trigger", function (e) {
        e.preventDefault();
        let videoUrl = $(this).attr("data-video");
        videoUrl = videoUrl.replace(/.*watch\?v=([^&]+).*/, "https://www.youtube.com/embed/$1");
        if (videoUrl) {
            console.log("設定するURL: " + videoUrl);
            $("#youtubeFrame").attr("src", videoUrl);
            $("#youtubeModal").fadeIn();
        } else {
            console.error("data-video属性が設定されていません");
        }
    });

    // **画像モーダルを開く**
    $(document).on("click", ".image-modal-trigger", function (e) {
        e.preventDefault();
        let imgSrc = $(this).attr("data-image");
        if (imgSrc) {
            console.log("表示する画像: " + imgSrc);
            $("#imageFrame").attr("src", imgSrc);
            $("#imageModal").fadeIn();
        } else {
            console.error("data-image属性が設定されていません");
        }
    });

    // **YouTubeモーダルを閉じる**
    $(document).on("click", ".close-modal, #youtubeModal", function () {
        $("#youtubeModal").fadeOut(() => {
            $("#youtubeFrame").attr("src", ""); // YouTubeの動画をリセット
        });
    });

    // **画像モーダルを閉じる**
    $(document).on("click", ".close-modal, #imageModal", function () {
        $("#imageModal").fadeOut(() => {
            $("#imageFrame").attr("src", ""); // 画像のsrcをクリア
        });
    });

    // **モーダル内のクリックを伝播させない**
    $(document).on("click", ".modal-content", function (e) {
        e.stopPropagation();
    });
});



// ===========================================
// ページトップボタン
// ===========================================
function adjustPageTopPosition() {
  let footer = document.querySelector(".l-footer");
  let pageTop = document.querySelector(".l-pagetop");

  if (!footer || !pageTop) return;

  let footerRect = footer.getBoundingClientRect(); // フッターの位置情報
  let windowHeight = window.innerHeight; // ウィンドウの高さ
  let offsetValue = window.innerWidth <= 500 ? 10 : 20; // PC:20px / スマホ:10px

  if (footerRect.top < windowHeight) {
    let newBottom = windowHeight - footerRect.top + offsetValue;
    pageTop.style.bottom = `${newBottom}px`;
  } else {
    pageTop.style.bottom = `${offsetValue}px`;
  }
}

window.addEventListener("scroll", adjustPageTopPosition);
window.addEventListener("resize", adjustPageTopPosition);

document.addEventListener("DOMContentLoaded", adjustPageTopPosition);


// ===========================================
// table横スクロール
// ===========================================
document.addEventListener("DOMContentLoaded", function() {
  const containers = document.querySelectorAll(".tableA01");
  const hints = document.querySelectorAll(".scroll-hint");

  function updateHintVisibility() {
    hints.forEach((hint, index) => {
      const container = containers[index];
      if (!hint || !container) return;

      if (window.innerWidth <= 676) {
        hint.style.display = "block";
        hint.style.opacity = "1";
        positionHint(container, hint);
      } else {
        hint.style.display = "none";
      }
    });
  }

  function positionHint(container, hint) {
    if (!hint || !container) return;
    const visibleWidth = container.clientWidth;
    hint.style.left = `${visibleWidth / 2}px`;
  }

  updateHintVisibility();

  window.addEventListener("resize", updateHintVisibility);

  containers.forEach((container, index) => {
    const hint = hints[index];
    if (!container || !hint) return;

    container.addEventListener("scroll", function() {
      hint.style.opacity = "0";
      setTimeout(() => {
        hint.style.display = "none";
      }, 500);
    }, { passive: true });
  });
});


// ===========================================
// アコーディオン（複数開閉可）
// ===========================================
jQuery(document).ready(function($) {
  function getHeaderHeight() {
    let header = $(".l-header");
    return header.length ? header.outerHeight(true) : 0; // ヘッダーの高さを取得
  }

  $(".js-accordion-header").click(function() {
    let content = $(this).next(".js-accordion-content");

    if (!content.is(":visible")) {
      // すでに開いている場合は閉じる
      content.stop(true, true).slideDown(300);
      $(this).addClass("open");
    } else {
      content.stop(true, true).slideUp(300);
      $(this).removeClass("open");
    }
  });

  function openAccordionFromHash() {
    let hash = window.location.hash;
    if (hash) {
      let target = $(hash);

      if (target.length && target.hasClass("p-faqItem")) {
        let header = target.find(".js-accordion-header").first();
        if (header.length) {
          header.addClass("open");
          header.next(".js-accordion-content").stop(true, true).slideDown(300);

          let headerHeight = getHeaderHeight();
          let offsetTop = header.offset().top - headerHeight - 20;

          $("html, body").animate({
            scrollTop: offsetTop
          }, 300, "swing");
        }
      }
    }
  }
  openAccordionFromHash();
});
