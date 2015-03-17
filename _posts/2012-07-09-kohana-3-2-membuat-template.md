---
layout: post
title: 'Kohana 3.2 : Membuat Template'
date: 2012-07-09 09:52:09.000000000 +07:00
categories:
- Kohana
- PHP
tags:
- kohana-3-2
- templating
status: publish
type: post
published: true
meta:
  _yoast_wpseo_metadesc: 'Kohana 3.2 : Membuat Template'
  _yoast_wpseo_focuskw: Kohana 3.2
  if_slider_image: http://www.jefri-p.com/wp-content/uploads/2012/04/logo-new.png
  _yoast_wpseo_linkdex: '81'
  _edit_last: '1'
  _syntaxhighlighter_encoded: '1'
  dsq_thread_id: '757393490'
  _thumbnail_id: '141'
author:
  login: admin
  email: jefri.p@gmail.com
  display_name: Jefri
  first_name: ''
  last_name: ''
excerpt: !ruby/object:Hpricot::Doc
  options: {}
---
<p>Dalam pembuatan sebuah website/sistem informasi template merupakan elemen penting dalam penyajian tampilan sebuah website, disini akan dijelaskan penggunaan template pada Kohana 3.2, agar pembuatan suatu website lebih efisien dan simpel.</p>
<p>Melanjutkan Blog <a title="PHP Framework : Mengenal Framework Kohana 3" href="http://www.jefri-p.com/2012/04/php-framework-mengenal-framework-kohana-3/">sebelumnya</a>, defaultnya template kohana membuat controller turunan dari Controller_Template, namun jika kita membuat 1 template untuk semua kita harus menyertakan title, javascript, css dll yang membuat wasting code. Oleh karena itu dibutuhkan sebuah suatu controller template baru yang akan diturunkan ke controller kita yang mempunyai template yang sama.</p>
<p>1. kita buat template kita yang berbentuk HTML (dalam hal ini menggunakan <a title="Twitter Bootstrap" href="https://github.com/twitter/bootstrap/" target="_blank">Twitter Bootstrap</a>), tinggal menambahkan beberapa tag php.<br />
<!--more--><br />
- title (string) : title dari page<br />
- scripts (array) : array dari javascripts yang dibutuhkan pada page<br />
- styles (array) : array dari CSS yang dibutuhkan pada page<br />
- content (string/array) : isi dari konten website</p>
<p>ok, just show the code :)</p>
<br />

{% highlight html+php startinline linenos %}
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Kohana 3.2 Templating with Twitter Bootstrap <?php echo ( ! empty($title)) ? Html::chars(" - ".$title) : ''; ?></title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="">
<meta name="author" content="">

<!-- Le styles -->
<style>
body '{
padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */
}'
</style>
<?php foreach ($styles as $file => $type) echo HTML::style($file, array('media' => $type)), "\n" ?>
<?php foreach ($scripts as $file) echo HTML::script($file), "\n" ?>

<!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
<!--[if lt IE 9]>
<script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
<![endif]-->

<!-- Le fav and touch icons -->
<link rel="shortcut icon" href="assets/ico/favicon.ico">
<link rel="apple-touch-icon-precomposed" sizes="144x144" href="assets/ico/apple-touch-icon-144-precomposed.png">
<link rel="apple-touch-icon-precomposed" sizes="114x114" href="assets/ico/apple-touch-icon-114-precomposed.png">
<link rel="apple-touch-icon-precomposed" sizes="72x72" href="assets/ico/apple-touch-icon-72-precomposed.png">
<link rel="apple-touch-icon-precomposed" href="assets/ico/apple-touch-icon-57-precomposed.png">
</head>

<body>

<div class="navbar navbar-fixed-top">
<div class="navbar-inner">
<div class="container">
<a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
<span class="icon-bar"></span>
<span class="icon-bar"></span>
<span class="icon-bar"></span>
</a>
<a class="brand" href="#">Jefri</a>
<div class="nav-collapse">
<ul class="nav">
<li class="active"><a href="#">Home</a></li>
<li><a href="#about">About</a></li>
<li><a href="#contact">Contact</a></li>
</ul>
</div><!--/.nav-collapse -->
</div>
</div>
</div>

<div class="container">
<?php echo $content ?>
</div> <!-- /container -->

</body>
</html>
{% endhighlight %}
</p>
<p>2. Buat Controller_Template baru untuk turunan controller yang akan kita pakai dengan template yang sama. sehingga akan terlihat seperti ini :</p>
<ul>
<ul>
<li>Controller_Template_Layout extends Controller_Template</li>
</ul>
</ul>
<ul>
<ul>
<ul>
<li>Controller_Page extends Controller_Template_Layout</li>
</ul>
</ul>
</ul>
<p>Jadi setiap controller akan meng-extends Controller_Template_Layout</p>
<p>
<br />
{% highlight php startinline linenos %}
<?php defined('SYSPATH') or die('No direct access allowed.');

class Controller_Template_Layout extends Controller_Template
{
public $template = 'template/layout';
/**
* The before() method is called before your controller action.
* In our template controller we override this method so that we can
* set up default values. These variables are then available to our
* controllers if they need to be modified.
*/
public function before()
{
	parent::before();
	$this->session = Session::instance();

	if ($this->auto_render)
	{
	// Initialize empty values
	$this->template->title = '';
	$this->template->content = '';
	$this->template->templates = '';

	$this->template->styles = array();
	$this->template->scripts = array();
	}
}

/**
* The after() method is called after your controller action.
* In our template controller we override this method so that we can
* make any last minute modifications to the template before anything
* is rendered.
*/
public function after()
{
	if ($this->auto_render)
	{
	$styles = array(
	'assets/css/bootstrap.css' => 'screen, projection',
	'assets/css/bootstrap-responsive.css' => 'screen, projection',
	);

	$scripts = array(
	'assets/js/jquery-1.7.2.min.js',
	'assets/js/bootstrap.js',
	);

	$this->template->styles = array_merge( $styles, $this->template->styles );
    $this->template->scripts = array_merge( $scripts, $this->template->scripts );
}
parent::after();
}

}
{% endhighlight %}</p>
<p>3. Membuat controller yang akan menggunakan template yang sudah kita buat.</p>
{% highlight php startinline linenos %}
<?php defined('SYSPATH') or die('No direct script access.');

class Controller_Page extends Controller_Template_Layout {

public function action_index()
{
	$this->template->title = __('Welcome to kohana 3.2 Template');

	$this->template->content = View::factory('page/home');
}

}
{% endhighlight %}
</p>
<p>Template untuk kohana 3.2 siap di pakai.<br />
<a href="/assets/templating.jpg"><img class="aligncenter size-large wp-image-141" title="templating" alt="kohana" src="/assets/templating-1024x583.jpg" width="608" height="346" /></a></p>
<p>Download melalui github <a href="https://github.com/jefrip/kohana-template">Kohana Template</a></p>
<p>Sumber Bacaan :<br />
- <a href="http://kerkness.ca/kowiki/doku.php">http://kerkness.ca/kowiki/doku.php</a><br />
- <a href="http://kohanaframework.org/3.2/guide/kohana/mvc/views">http://kohanaframework.org/3.2/guide/kohana/mvc/views</a></p>
