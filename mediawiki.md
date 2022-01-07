# biligame-mediawiki笔记

前置知识：[bwiki帮助:目录](https://wiki.biligame.com/wiki/%E5%B8%AE%E5%8A%A9:%E7%9B%AE%E5%BD%95) 

用 MW 写文章写 wiki 最好需要知道点语法知识

==黄金宝典：**尽量不要增加维护成本**==

## `[]`语法

可以缺省一些条件

| 语法                                                         | 含义                                                    |
| ------------------------------------------------------------ | ------------------------------------------------------- |
| `[[xxx]]`                                                    | 跳转到xxx页面                                           |
| `[[xxx|yyy]]`                                                | 跳转到xxx页面，但显示的文字是yyy                        |
| `[xxx yyy]`                                                  | 跳转到外链xxx，但显示的文字是yyy                        |
| `[[分类:xxx]]`                                               | 将页面分类为xxx                                         |
| `[[file:xxx]]`或`[[文件:xxx]]`                               | 显示名为xxx的文件                                       |
| `[[file:xxx|显示的文件名|600px|center|link=图片链接地址]]`例如`[[file:logo.png|logo|300x300px|class=img-kk|link=none]]` | `|`是管道符，可以认为是入参间隔符，后面的参数都是可选的 |

## `{}`语法

[帮助:变量](https://wiki.biligame.com/wiki/%E5%B8%AE%E5%8A%A9:%E5%8F%98%E9%87%8F) 

[Help:Magic words](https://www.mediawiki.org/wiki/Help:Magic_words)

| 语法                 | 含义                                                         |
| -------------------- | ------------------------------------------------------------ |
| `{{模板名|参数}}`    | 加载在**模板**(template)名字空间内的内容，可以传入参数       |
| `{{模板名|xxx=yyy}}` | 可以通过指定参数名来给模板传入名xxx、值为yyy的数据，通常在正式的模板里需要这样做，否则容易参数错乱 |
| `{{:页面名}}`        | 加载不在模板名字空间内的内容，即普通页面的内容，同样可以传入参数 |
| `{{{1|}}}`           | 读取通过管道传入的第1个参数（没有第0个参数）                 |
| `{{{xxx|}}}`         | 读取通过管道传入的名为xxx的数据的值                          |
| `{{板块|xxx}}`       | bwiki的教程里有让大家用这个懒人包，这个其实是官方写好的一个模板，也可以改 |

使用管道变量：`{{{name1|name2|name3...}}}`，多个变量之间使用管道符`|`进行分隔。管道变量相当于函数传参。

### {{#xxx:}}

这是 SMW 里非常重要的一块内容——解析函数，时常需要这个来给 wiki 搞点花样的东西，熟练使用这个能减少 JS 的使用。但不熟练的使用，在 pcr 的历史里，把两个字段用`#switch`做一一映射，五百多个值，放在两个页面里，大大增加维护成本，不如用`#ask`或更好的`#show`来查找。

- 用法

  ```javascript
  {{#function:
  ...
  }}
  ```

[bwiki帮助:SMW](https://wiki.biligame.com/wiki/%E5%B8%AE%E5%8A%A9:SMW) 使用SMW语义来处理一些数据向的内容。

[bwiki帮助:解析函数](https://wiki.biligame.com/wiki/%E5%B8%AE%E5%8A%A9:%E8%A7%A3%E6%9E%90%E5%87%BD%E6%95%B0) 

[thwiki.cc/帮助:解析函数](https://thwiki.cc/%E5%B8%AE%E5%8A%A9:%E8%A7%A3%E6%9E%90%E5%87%BD%E6%95%B0) 

[cq/肉卷丝的笔记](https://wiki.biligame.com/cq/%E8%A7%A3%E6%9E%90%E5%99%A8%E5%87%BD%E6%95%B0) 

mediawiki.org 是MW的官方网站，里面有很棒的教程，但不要使用里面的搜索引擎，不如直接 google 查找教程。

[mediawiki.org/mw.loader.load](https://www.mediawiki.org/wiki/ResourceLoader/Core_modules#mw.loader.load) 

[mediawiki.org/Help:Extension:ParseFunctions](https://www.mediawiki.org/wiki/Help:Extension:ParserFunctions#) 

[mediawiki.org/Extension:Loops](https://www.mediawiki.org/wiki/Extension:Loops) 

[mediawiki.org/Extension:StringFunctions/zh](https://www.mediawiki.org/wiki/Extension:StringFunctions/zh) （explode分割字符串非常好用）

[mediawiki.org/Manual:Interface/JavaScript](https://www.mediawiki.org/wiki/Manual:Interface/JavaScript) 

[semantic-mediawiki.org](https://www.semantic-mediawiki.org/wiki/Semantic_MediaWiki/zh-hans) 

[bwikiAPI沙盒](https://wiki.biligame.com/wiki/%E7%89%B9%E6%AE%8A:ApiSandbox) 

[灰机wiki/帮助:解析函数](https://www.huijiwiki.com/wiki/%E5%B8%AE%E5%8A%A9:%E8%A7%A3%E6%9E%90%E5%99%A8%E5%87%BD%E6%95%B0#) 

[mw.Api().edit()](https://doc.wikimedia.org/mediawiki-core/master/js/#!/api/mw.Api.plugin.edit) 

[mw.Api()](https://doc.wikimedia.org/mediawiki-core/master/js/#!/api/mw.Api) 

常用的`function`有`#set` `#ask` `#show` `#info` `#switch` `#widget`等，可以等到用的时候再了解它们。

#### #set

`#set`给页面设置属性，可以通过浏览页面属性来看到页面的属性，可以给一个属性名设置多个属性，给页面设置属性后，可以通过`#ask`查找属性来定位到该页面，定位到这些页面后，就可以获取这些页面的其他属性，只需要更新这些页面及其属性，使用`#ask`显示的页面就能同步更新，维护成本低。

一个属性可以设置多个值，这个其实是非常香的，以目前测试来看，值还是有序的，以 pcr 为例，一个地图会掉落多种装备，现在的需求是要查询某种装备在哪些地图里掉落，如果不分开设置值的话，`#ask`使用模糊匹配，很有可能会因为字符串太长而没匹配上；值分开设置的话，就不会有这种匹配问题。

**扩展** 在现阶段的 bwiki 表格，使用 jQuery 提供筛选功能，如果不使用数据查询那个`#wedge`调用`#ask`模糊匹配，那只能用 jQuery 的全字匹配，不过在设置`data-param`时，可以给一个`data-param`设置多个值，这就增大了匹配成功的机会，筛选项能够筛选的字段更多。

在 pcr 的历史里，通过`#arraymap`来遍历设置属性……走弯路了啊，就是角色外号那个，写这篇文章的时候顺手改掉了。

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

#### #switch



```javascript
{{#switch: 比较字串
| 情况字串1 = 返回结果1
| 情况字串2 = 返回结果2
| ...
| 情况字串n = 返回结果n
| 默认结果
}}
```

#### #if



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

#### #array



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
 // 好像会自动strip()
```

## 其他

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

但当页面作为模板时，不建议这样使用，这个 CSS 会复制很多份，建议放在 MediaWiki 里，通过 ResourceLoader 引用。但是可以通过`#vardefine`来规避 CSS 的重复定义，具体代码如下：

```css
{{#if: {{#varexists: 合成树样式 }} 
| {{#vardefine: 合成树样式|{{#expr:{{#var: 合成树样式}} + 1}} }} 
| {{#vardefine: 合成树样式|1}} {{#css:..............}} 
}}

```

## ResourceLoader

加载资源，资源需要在`MediaWiki`这个名字空间下。

`MediaWiki:name.js`/`MediaWiki:name.css`，支持 jQuery。

[用法](https://wiki.biligame.com/wiki/%E6%A8%A1%E6%9D%BF:ResourceLoader)，例如

```javascript
{{ResourceLoader|MediaWiki:Gacha|true}}
{{ResourceLoader|MediaWiki:Gacha|false|text/javascript}}
{{ResourceLoader|MediaWiki:Gacha.js}}
```

这个，有半小时的缓存期，因此建议本地调试后再放到 wiki 中。下面的 Widget 没有缓存期，但性能低一些。

## Widget

[动态查询](https://wiki.biligame.com/wiki/%E5%8A%A8%E6%80%81%E6%9F%A5%E8%AF%A2) 

这个非常好用，可以结合 mw.Api() 玩出做出丰富的功能，而且是在页面加载后才会加载 Widget。但是，可能会在 jQuery 加载出来前加载 Widget，所以把 jQuery 的代码放在有交互操作的部分吧。

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

- 表格对`|`非常敏感，一般使用`{{!}}`代替解析函数里的`|`，防止被解析为表格里的`|`。

## Form

[表单](https://www.mediawiki.org/wiki/Extension:Page_Forms)，可以在`Form`名字空间下创建一个表单，相当于在`Template`（模板）名字空间下创建一个模板。

创建表单，在`特殊:创建表单`里，根据名字添加元素，元素可以是模板或者章节，也就是说一个表单可以使用多个模板，并且可以自由定义模板字段的默认值、值类型、填写位置等等。创建的表单类似于[pcr/Form:添加角色2](https://wiki.biligame.com/pcr/Form:%E6%B7%BB%E5%8A%A0%E8%A7%92%E8%89%B22)。

有了表单之后，可以在表单里填写页面名，点击<button>创建或编辑</button>将会跳转到一个新的链接。例如[pcr/特殊:编辑表格/添加角色2/凯露（新年）](https://wiki.biligame.com/pcr/%E7%89%B9%E6%AE%8A:%E7%BC%96%E8%BE%91%E8%A1%A8%E6%A0%BC/%E6%B7%BB%E5%8A%A0%E8%A7%92%E8%89%B22/%E5%87%AF%E9%9C%B2%EF%BC%88%E6%96%B0%E5%B9%B4%EF%BC%89)，跳转后的链接包含使用的表单和目的页面，在这个链接显示的页面里，可以使用表单来编辑页面。

优点：可视化编辑，总比纯文字要强。

缺点：依赖于模板和表单，像写攻略文章这样的活是不能用表单的。

### Input types

在`Form`里，通过`Form tags`来给模板字段输入值，后面可以添加许多自定义的输入类型 ([Input types](https://www.mediawiki.org/wiki/Extension:Page_Forms/Input_types))，例如`{{{field|字段|size=18}}}`设置该`field`输入框的宽度为18。以下 MediaWiki & Cargo quick reference 第二页一整页都是教程。

![img](https://upload.wikimedia.org/wikipedia/mediawiki/4/4e/Cargo_quick_reference.png)

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

