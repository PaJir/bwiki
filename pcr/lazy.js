// lazy load image
// example: [[file:加载中.gif|600px|class=img-kk img-lazy|alt={{filepath:Chr_110631.jpg}}]]
$(document).ready(function () {
    var eles = document.querySelectorAll(".img-lazy"); // 获取所有列表元素
    // 监听回调
    var lazycallback = function (entries) {
        entries.forEach(function (item) {
            // 出现到可视区
            if (item.intersectionRatio > 0) {
                var ele = item.target;
                var imgSrc = ele.getAttribute("alt");
                if (imgSrc) {
                    // 预加载
                    var img = new Image();
                    img.addEventListener(
                        "load",
                        function () {
                            ele.src = imgSrc;
                        },
                        false
                    );
                    ele.src = imgSrc;
                    // 加载过清空路径，避免重复加载
                    ele.removeAttribute("alt");
                }
            }
        });
    };
    var observer = new IntersectionObserver(lazycallback);

    // 列表元素加入监听
    eles.forEach(function (item) {
        observer.observe(item);
    });
});
