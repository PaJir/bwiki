# biligame教程整理

前置知识：[帮助:目录](https://wiki.biligame.com/wiki/%E5%B8%AE%E5%8A%A9:%E7%9B%AE%E5%BD%95) 

### `[[]]`语法一览

可以缺省一些条件

```javascript
[[分类:分类名词]]
[[file:文件名.png|显示的文件名|600px|center|link=图片链接地址]]
[[文件:文件名.格式|显示文字|300px(宽度)|x300px(高度)|class=(类样式名)|link=(需要跳转链接)]]]
```

### `{{}}`语法一览

[帮助:变量](https://wiki.biligame.com/wiki/%E5%B8%AE%E5%8A%A9:%E5%8F%98%E9%87%8F) 

```javascript
{{颜色|红|内容}}
{{背景|图片地址}}
{{模板名|参数}}
{{模板名}}
{{板块|xxx}}也是一个模板，只是官方有比较完善的懒人包
```

使用管道变量：`{{{name1|name2|name3...}}}`，多个变量之间使用管道符`|`进行分隔。管道变量相当于函数传参。

## SMW、解析函数

- 用法

  ```javascript
  {{#function:
  ...
  }}
  ```

[帮助:SMW](https://wiki.biligame.com/wiki/%E5%B8%AE%E5%8A%A9:SMW) 使用SMW语义来处理一些数据向的内容。

[thwiki.cc/帮助:解析函数](https://thwiki.cc/%E5%B8%AE%E5%8A%A9:%E8%A7%A3%E6%9E%90%E5%87%BD%E6%95%B0) 

[肉卷丝的笔记](https://wiki.biligame.com/cq/%E8%A7%A3%E6%9E%90%E5%99%A8%E5%87%BD%E6%95%B0) 

[mw.loader.load](https://www.mediawiki.org/wiki/ResourceLoader/Core_modules#mw.loader.load) 

[semantic-mediawiki.org](https://www.semantic-mediawiki.org/wiki/Semantic_MediaWiki/zh-hans) 

常用的`function`有`#set` `#ask` `#show` `#info` `#switch` `#widget`等，可以等到用的时候再了解它们。

```javascript
 {{#set:
 |属性名1=值1,值2|+sep=,
 |属性名2=值1;值2;值3;|+sep=;
 |属性名3=值1
 |属性名3=值2
 |属性名4=值1|值2|值3
 |属性名5=值1
 …
 }}
```

```javascript
{{#switch: 比较字串
| 情况字串1 = 返回结果1
| 情况字串2 = 返回结果2
| ...
| 情况字串n = 返回结果n
| 默认结果
}}
```

```javascript
{{#if: 测试字串 
| 字串非空输出值 
| 字串空（或只有空白字符）输出值 
}}
{{#if: 参数1 
| 参数2 
| 参数3 
}}
```

```javascript
格式
{{#arraymap: 字串
| 分隔符（默认为“,”） 
| 代号 
| 格式字串 
| 输出分隔符（默认为“, ”，注意有空格） 
}}
例子
{{#arraymap:22;33;小电视
|;
|@
|<font color=red>@</font>
|，
 }} → 22，33，小电视
```

## 扩展

[InputBox](https://www.mediawiki.org/wiki/Extension:InputBox/zh) 

[导航栏](https://wiki.biligame.com/gt/MediaWiki:Sidebar) 

## CSS

用了bootstrap啊，[bootstrap菜鸟教程](https://www.runoob.com/bootstrap/bootstrap-tutorial.html) 

bootstrap代码：`<var> <pre> <pre class="pre-scrollable"> <code>`

轮播 `<ol>`

[how can I move a rows div into another row](https://stackoverflow.com/questions/34793979/bootstrap-how-can-i-move-a-rows-div-into-another-row) （不好用）

class: `col-sm-3`, `col-sm-12`, `xs, sm, md, lg, xl` 

在编辑页面时，可以通过 SMW 提供的function来使得部分 CSS 样式附加在该页面上，例如：

```javascript
{{#css:
.p {
    height: 20px;
}
}}
```

但当页面作为模板时，不建议这样使用，这个 CSS 会复制很多份，建议放在 MediaWiki 里，通过 ResourceLoader 引用。

## JS

`MediaWiki:name.js`，支持 jQuery。

## ResourceLoader

[用法](https://wiki.biligame.com/wiki/%E6%A8%A1%E6%9D%BF:ResourceLoader)，例如

```javascript
{{ResourceLoader|MediaWiki:Gacha|true}}
{{ResourceLoader|MediaWiki:Gacha|false|text/javascript}}
{{ResourceLoader|MediaWiki:Gacha.js}}
```

这个，有半小时的缓存期，因此建议本地调试后再放到 wiki 中。下面的 Widget 没有缓存期，但性能低一些。

## Widget

[动态查询](https://wiki.biligame.com/wiki/%E5%8A%A8%E6%80%81%E6%9F%A5%E8%AF%A2) 

## 表格

- class

  ```javascript
  wikitable sortable mw-collapsible mw-made-collapsible mw-collapsed
  ```

  |      |                                                              |                                                              |
  | :--: | ------------------------------------------------------------ | ------------------------------------------------------------ |
  | {\|  | 表格起始，必需                                               | 可以在这一行添加整个表格的预制样式 例如`{|class="wikitable"....`，wikitable就是mediawiki预制好的整体表格样式。 在这一行里还需可以添加`style="...."`来定义表格内的元素。具体语法需要查阅css和html相关的文档。 |
  | \|+  | 表格标题，*选用*；每张表格只能出现一次且介于表格起始与第一行 | 这张表格的基本语法一行就使用的这个语法，表格内容外的一个表格标题。 |
  | \|-  | 表格行，*第一行选用* -- wiki 引擎会假设是第一行              | 同样可以在这一行里添加`style="...."`来控制这一行的行内样式   |
  |  !   | 表格标题 储存格， *选用*。 可以使用（!!）在同一行加入接续的表格标题或是单独使用（!）换新的一行 。 |                                                              |
  |  \|  | 表格数据调用，*可选*。 可以使用（\|\|）接续表格资料储存格或是单独使用（\|）。 |                                                              |
  | \|}  | 表格末尾，必要                                               |                                                              |

- 示例1

  ```javascript
  {| class="wikitable"
  |-
  ! 标题文字 !! 标题文字 !! 标题文字
  |-
  | 示例 || 示例 || 示例
  |-
  | 示例 || 示例 || 示例
  |-
  | 示例 || 示例 || 示例
  |}
  ```

- 示例2

  ```javascript
  {{信息栏
  |位置=right
  |图片=
  |图片介绍=
  |标题栏颜色=#5bc0de
  |属性1=
  |属性1内容=
  |属性2=
  |属性2内容=
  |属性3=
  |属性3内容=
  |属性4=
  |属性4内容=
  |属性5=
  |属性5内容=
  |属性6=
  |属性6内容=
  |属性7=
  |属性7内容=
  |额外属性1=
  |额外属性1内容=
  }}
  ```

- 注意，预览结果若不是预期的效果，可能是在该换行的地方不换行，不该换行的地方换行。

## 页面快捷键

| 编辑             | 命令                 |
| ---------------- | -------------------- |
| 编辑页面         | ALT+SHIFT+E          |
| 删除页面         | ALT+SHIFT+D          |
| 保存页面         | ALT+SHIFT+S或者ALT+S |
| 显示预览         | ALT+SHIFT+P或者ALT+P |
| 显示更改         | ALT+SHIFT+V或者ALT+V |
| 显示页面历史     | ALT+SHIFT+H或者ALT+H |
| 查看页面手机版本 | CTRL+SHIFT+E         |

## 坎公

$$
秒伤害=攻击\times武器攻速补偿系数\times(1+暴击率\times(暴击倍数-1))\\
*武器攻速补偿系数:单手剑3, 双手剑2.5, 步枪不定,弓2,篮子4, 法杖3, 拳套4, 爪子3.5\\
*组队效果、五星效果和专武效果不计入秒伤害计算\\
防御=(基础防御+装备防御)\times(1+觉醒增幅+图鉴增幅+装备增幅)\\
韧性=血量\times\frac{100+防御}{100}+伤害减免\times10\\
伤害=输出\times\frac{100}{100+防御}\times(1-属性抗性)-伤害减免
$$

