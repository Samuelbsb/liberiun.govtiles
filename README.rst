*****************
liberiun.govtiles
*****************

.. contents:: Conte�do
   :depth: 2

Introdu��o
----------

Este pacote contem alguns tiles desenvolvidos pela Liberiun
para serem usados nos portais do Governo Federal.

Estado deste pacote
-------------------

O **liberiun.govtiles** est� est�vel e atualmente � usado nos portais da Ouvidoria e do PPA.

.. image:: https://travis-ci.org/liberiun/liberiun.govtiles.png?branch=master
	:target: https://travis-ci.org/liberiun/liberiun.govtiles

.. image:: https://coveralls.io/repos/liberiun/liberiun.govtiles/badge.png
	:target: https://coveralls.io/r/liberiun/liberiun.govtiles

Instala��o
----------

Para habilitar a instala��o deste produto em um ambiente que utilize o
buildout:

1. Editar o arquivo buildout.cfg (ou outro arquivo de configura��o) e
   adicionar o pacote ``liberiun.govtiles`` � lista de eggs da instala��o::

        [buildout]
        ...
        eggs =
            liberiun.govtiles

2. Ap�s alterar o arquivo de configura��o � necess�rio executar
   ''bin/buildout'', que atualizar� sua instala��o.

3. Reinicie o Plone

4. Instale o produto por meio do painel de controle na op��o **Complementos**.