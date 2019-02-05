---
layout: post
title: 'Importing database (Oracle) to Solr'
date: 2019-02-05 10:10:15.000000000 +07:00
categories:
- Solr
tags:
- solr
- oracle
- java
- import
status: publish
type: post
published: true
author: admin
excerpt_separator: <!--more-->
---


[![Solr]({{ site.baseurl }}/assets/solr.png)](http://lucene.apache.org/solr/){:target="_blank"}

Solr adalah platform open source untuk search yang dibuat di atas Apache Lucene.

Jika ada memiliki data di database (MySQL, PostgreSQL, Oracle, MsSQL).

Disini kita akan coba import data Oracle menggunakan fitur Solr yakni Data Import Handler (DIH)
<!--more--><br />
Saya asumsikan Anda sudah menginstall Oracle 11g, Solr (7.4.0), dan Java (dalam hal ini Java 8).

## Konfigurasi Datasource Database Oracle
1. [Download](https://www.oracle.com/technetwork/database/application-development/jdbc/downloads/index.html) dan copy file jar Oracle Database JDBC driver ke server Solr Anda (semisal /solr/solr-6.4.0/server/). 
> Jika Anda menggunakan JDK 6 maka gunakan jar ojdbc6.jar, sebaliknya jika Anda menggunakan JDK 7 & JDK 8 gunakan ojdbc7.jar karna akan error jika salah menggunakan library.

2. Konfigurasikan Solr [schema.xml](https://gist.githubusercontent.com/jefrip/8c3fa95bb84ddc5d3a19a76d0df33f5e/raw/a24bf9a09df54cb86d58ec33e8f6f99eb340d320/schema.xml) (asumsi folder solr Anda berada pada direktori `/solr/solr-6.4.0/server/solr/`) maka buat lah folder baru untuk configset (config, data, lib) pada `/solr/solr-6.4.0/server/solr/configsets/oracle_configs/conf`. Tambahkan field-field apa saja yang akan di index ke dalam Solr
3. Konfigurasikan Oracle data source ke dalam Solr file [data-config.xml](https://gist.githubusercontent.com/jefrip/abaea5ce2141459d5ecb9f92a4c77ef5/raw/e19a1b66d330471063c1142dc37cdf29925291b5/data-config.xml) pada `/solr/solr-6.4.0/server/solr/configsets/oracle_configs/conf` data source kurang lebih berisi informasi koneksi ke data source Oracle, username, password. data-config.xml juga berisi query Anda mengambil data dari Oracle yang akan di import ke Solr.
4. Konfigurasikan file solrconfig.xml dan karena kita menggunakan schema.xml maka didalamnya harus ada informasi requestHandler org.apache.solr.handler.dataimport.DataImportHandler, schemaFactory ClassicIndexSchemaFactory juga dalam solrconfig.xml kita sertakan unique id, semisal dalam hal ini menggunakan uuid generator.
5. Restart Solr server untuk mereload lib dan konfigurasi yang sudah kita taruh `bin/solr restart`

## Menjalankan data import di Solr
1. Buka [http://localhost:8983/solr/](http://localhost:8983/solr/) Anda akan di arahkan ke Solr Admin Console.
2. Pilih menu data import pada Solr Admin Console, ada di URL `/dataimport`
3. Pada menu data import pilih `full-import` ceklis `clean, commit`
4. Klik tombol `Execute` maka Anda akan otomatis melakukan import data dari Oracle ke Solr.
5. Jika sudah selesai mengimport data Anda dapat melihat hasil import data Anda melalui menu `Query`

Selamat mencoba.