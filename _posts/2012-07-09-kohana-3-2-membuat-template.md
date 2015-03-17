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
{% raw %}
&lt;!DOCTYPE html&gt;<br />
&lt;html lang=&quot;en&quot;&gt;<br />
  &lt;head&gt;<br />
    &lt;meta charset=&quot;utf-8&quot;&gt;<br />
    &lt;title&gt;Kohana 3.2 Templating with Twitter Bootstrap &lt;?php echo ( ! empty($title)) ? Html::chars(&quot; - &quot;.$title) : ''; ?&gt;&lt;/title&gt;<br />
&lt;meta name=&quot;viewport&quot; content=&quot;width=device-width, initial-scale=1.0&quot;&gt;<br />
&lt;meta name=&quot;description&quot; content=&quot;&quot;&gt;<br />
&lt;meta name=&quot;author&quot; content=&quot;&quot;&gt;</p>
<p>&lt;!-- Le styles --&gt;<br />
&lt;style&gt;<br />
body '{<br />
padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */<br />
}'<br />
&lt;/style&gt;<br />
&lt;?php foreach ($styles as $file =&gt; $type) echo HTML::style($file, array('media' =&gt; $type)), &quot;\n&quot; ?&gt;<br />
&lt;?php foreach ($scripts as $file) echo HTML::script($file), &quot;\n&quot; ?&gt;</p>
<p>&lt;!-- Le HTML5 shim, for IE6-8 support of HTML5 elements --&gt;<br />
&lt;!--[if lt IE 9]&gt;<br />
&lt;script src=&quot;http://html5shim.googlecode.com/svn/trunk/html5.js&quot;&gt;&lt;/script&gt;<br />
&lt;![endif]--&gt;</p>
<p>&lt;!-- Le fav and touch icons --&gt;<br />
&lt;link rel=&quot;shortcut icon&quot; href=&quot;assets/ico/favicon.ico&quot;&gt;<br />
&lt;link rel=&quot;apple-touch-icon-precomposed&quot; sizes=&quot;144x144&quot; href=&quot;assets/ico/apple-touch-icon-144-precomposed.png&quot;&gt;<br />
&lt;link rel=&quot;apple-touch-icon-precomposed&quot; sizes=&quot;114x114&quot; href=&quot;assets/ico/apple-touch-icon-114-precomposed.png&quot;&gt;<br />
&lt;link rel=&quot;apple-touch-icon-precomposed&quot; sizes=&quot;72x72&quot; href=&quot;assets/ico/apple-touch-icon-72-precomposed.png&quot;&gt;<br />
&lt;link rel=&quot;apple-touch-icon-precomposed&quot; href=&quot;assets/ico/apple-touch-icon-57-precomposed.png&quot;&gt;<br />
&lt;/head&gt;</p>
<p>&lt;body&gt;</p>
<p>&lt;div class=&quot;navbar navbar-fixed-top&quot;&gt;<br />
&lt;div class=&quot;navbar-inner&quot;&gt;<br />
&lt;div class=&quot;container&quot;&gt;<br />
&lt;a class=&quot;btn btn-navbar&quot; data-toggle=&quot;collapse&quot; data-target=&quot;.nav-collapse&quot;&gt;<br />
&lt;span class=&quot;icon-bar&quot;&gt;&lt;/span&gt;<br />
&lt;span class=&quot;icon-bar&quot;&gt;&lt;/span&gt;<br />
&lt;span class=&quot;icon-bar&quot;&gt;&lt;/span&gt;<br />
&lt;/a&gt;<br />
&lt;a class=&quot;brand&quot; href=&quot;#&quot;&gt;Jefri&lt;/a&gt;<br />
&lt;div class=&quot;nav-collapse&quot;&gt;<br />
&lt;ul class=&quot;nav&quot;&gt;<br />
&lt;li class=&quot;active&quot;&gt;&lt;a href=&quot;#&quot;&gt;Home&lt;/a&gt;&lt;/li&gt;<br />
&lt;li&gt;&lt;a href=&quot;#about&quot;&gt;About&lt;/a&gt;&lt;/li&gt;<br />
&lt;li&gt;&lt;a href=&quot;#contact&quot;&gt;Contact&lt;/a&gt;&lt;/li&gt;<br />
&lt;/ul&gt;<br />
&lt;/div&gt;&lt;!--/.nav-collapse --&gt;<br />
&lt;/div&gt;<br />
&lt;/div&gt;<br />
&lt;/div&gt;</p>
<p>&lt;div class=&quot;container&quot;&gt;<br />
&lt;?php echo $content ?&gt;<br />
&lt;/div&gt; &lt;!-- /container --&gt;</p>
<p>&lt;/body&gt;<br />
&lt;/html&gt;<br />

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
<p>[code lang="php"]
<br />
&lt;?php defined('SYSPATH') or die('No direct access allowed.');</p>
<p>  class Controller_Template_Layout extends Controller_Template<br />
  {<br />
      public $template = 'template/layout';<br />
      /**<br />
* The before() method is called before your controller action.<br />
* In our template controller we override this method so that we can<br />
* set up default values. These variables are then available to our<br />
* controllers if they need to be modified.<br />
*/<br />
      public function before()<br />
      {<br />
parent::before();<br />
$this-&gt;session = Session::instance();</p>
<p>   if ($this-&gt;auto_render)<br />
   {<br />
   // Initialize empty values<br />
   $this-&gt;template-&gt;title = '';<br />
   $this-&gt;template-&gt;content = '';<br />
$this-&gt;template-&gt;templates = '';</p>
<p>   $this-&gt;template-&gt;styles = array();<br />
   $this-&gt;template-&gt;scripts = array();<br />
        }<br />
      }</p>
<p>      /**<br />
* The after() method is called after your controller action.<br />
* In our template controller we override this method so that we can<br />
* make any last minute modifications to the template before anything<br />
* is rendered.<br />
*/<br />
      public function after()<br />
      {<br />
if ($this-&gt;auto_render)<br />
{<br />
$styles = array(<br />
'assets/css/bootstrap.css' =&gt; 'screen, projection',<br />
'assets/css/bootstrap-responsive.css' =&gt; 'screen, projection',<br />
);</p>
<p>$scripts = array(<br />
'assets/js/jquery-1.7.2.min.js',<br />
'assets/js/bootstrap.js',<br />
);</p>
<p>$this-&gt;template-&gt;styles = array_merge( $styles, $this-&gt;template-&gt;styles );<br />
$this-&gt;template-&gt;scripts = array_merge( $scripts, $this-&gt;template-&gt;scripts );<br />
}<br />
parent::after();<br />
      }</p>
<p>  }<br />
[/code]</p>
<p>3. Membuat controller yang akan menggunakan template yang sudah kita buat.</p>
<p>[code lang="php"]<br />
&lt;?php defined('SYSPATH') or die('No direct script access.');</p>
<p>class Controller_Page extends Controller_Template_Layout {</p>
<p>public function action_index()<br />
{<br />
$this-&gt;template-&gt;title = __('Welcome to kohana 3.2 Template');</p>
<p>   $this-&gt;template-&gt;content = View::factory('page/home');<br />
}</p>
<p>}<br />
[/code]</p>
<p>Template untuk kohana 3.2 siap di pakai.<br />
<a href="/assets/templating.jpg"><img class="aligncenter size-large wp-image-141" title="templating" alt="kohana" src="/assets/templating-1024x583.jpg" width="608" height="346" /></a></p>
<p>Download melalui github <a href="https://github.com/jefrip/kohana-template">Kohana Template</a></p>
<p>Sumber Bacaan :<br />
- <a href="http://kerkness.ca/kowiki/doku.php">http://kerkness.ca/kowiki/doku.php</a><br />
- <a href="http://kohanaframework.org/3.2/guide/kohana/mvc/views">http://kohanaframework.org/3.2/guide/kohana/mvc/views</a></p>
