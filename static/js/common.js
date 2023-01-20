$(function () {  // ここはお約束

function hamburger() {
  document.getElementById('line1').classList.toggle('line_1');
  document.getElementById('line2').classList.toggle('line_2');
  document.getElementById('line3').classList.toggle('line_3');
  document.getElementById('nav').classList.toggle('in');
}
document.getElementById('hamburger').addEventListener('click' , function () {
  hamburger();
} );
  // $("#txt").text("ノードを更新");
  // $("#jsbtn").on('click', function() {
  //   $("#sec1 h1").text("ノードを更新");
  // });

  //   $(".hum_menu").on('click', function() {
  //   $("header").toggleClass("open");
  // });
  //
  // $("#jsbtn").on('click' , function(){
  // $("#sec1 h1").css("color" , "red");
  // });





  /////////////////////////////
  // ここから課題のサンプルコード//
  ////////////////////////////

  // スマホレイアウトのときに、ハンバーガーボタンを押すとメニューを表示させる
  $('.hum_menu').on('click', function () {
    $('header').toggleClass('open');
  });

  // 課題1解答 
  // グローバルメニュー国際化
  $("#lng-ja").on('click', function () {
    $("#menu-sec1").text('見出しのエリア');
    $("#menu-sec2").text('flexのエリア');
    $("#menu-sec3").text('センタリングエリア');
    $("#menu-sec4").text('制作実績');
  });

  $("#lng-en").on('click', function () {
    $('#menu-sec1').text('Heading');
    $('#menu-sec2').text('Flex');
    $('#menu-sec3').text('Centering');
    $('#menu-sec4').text('Portfolio');
  });


  // 課題3解答 
  // 制作実績画像サイズ拡大
  $("#size-up").on('click', function () {
    $("#sec4 img").css("width", "600px");
  });


  // 課題4解答 
  // ブロックエリアをボタンで追加
  function appendFlex() {
    var appendedDiv = '<div class="flex_area_padding"><h2>flexを使って左から詰めていく</h2><p>ここにflexに関してのテキストが入りますここにflexに関してのテキストが入ります ここにflexに関してのテキストが入りますここにflexに関してのテキストが入ります ここにflexに関してのテキストが入りますここにflexに関してのテキストが入ります ここにflexに関してのテキストが入りますここにflexに関してのテキストが入ります</p></div>'
    $(".flex_area").append(appendedDiv);
  }

  $("#append").on('click', function () {
    appendFlex();
  });


  // 課題5解答 
  // 制作実績の画像を変更する
  //(全ての画像を更新する)
  $("#img-change").on('click', function () {
    $("#sec4 img").attr("src", "/static/img/thumb_01.png"); // 好きな画像を用意してください
  });


  // 課題6解答 
  // 入力した数字（1~10）でブロックエリアを追加
  $("#appendDivNum").on("click", function (e) {
    // イベントをキャンセルしてページ最上部への移動を防ぐ
    e.preventDefault();
    // 入力フォームの値を取得
    var textForm = $("#textForm").val();
    // 入力フォームから入力された値は「文字列型」
    console.log(typeof textForm);
    // 入力されたものは「文字列型」なので「数値型」に型変換
    textForm = Number(textForm);
    console.log(typeof textForm);

    if (textForm > 0 && textForm < 11 && Number.isInteger(textForm)) {
      console.log("1~10までの整数です")
      for (var i = 0; i < textForm; i++) {
        appendFlex();
        $("#attention").css("display", "none");
      }
    } else {
      console.log("文字列または0または11以上の整数または小数です")
      $("#attention").css("display", "block");
    }
  });


  ////////////////////////////
  // ここからプラグイン用の記述 //
  ///////////////////////////

  // スライドイン
  $(window).fadeThis();

  //ドロワーメニュー
  $(".drawer").drawer();






  // こちらは現在使われておりません

  //   背景色変更
  // $("#bg-blue").on('click', function() {
  //   $('body').removeClass("bg-red"); // 青にする前に赤を取り除く
  //   $('body').toggleClass("bg-blue");
  // });

  // $("#bg-red").on('click', function() {
  //   $('body').removeClass("bg-blue"); // 赤にする前に青を取り除く
  //   $('body').toggleClass("bg-red");
  // });

  // 制作実績の画像を変更する
  // (特定の画像を更新する)
  // $("#img-change").on('click', function() {
  //  $("#change-target").attr("src", "img/change_img.jpg");
  // });


});