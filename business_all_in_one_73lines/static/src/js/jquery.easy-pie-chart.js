(function() {
    ! function(a) {
        a.easyPieChart = function(b, c) {
            var d, e, f, g, h, i, j, k = this;
            return this.el = b, this.$el = a(b), this.$el.data("easyPieChart", this), this.init = function() {
                var b;
                return k.options = a.extend({}, a.easyPieChart.defaultOptions, c), b = parseInt(k.$el.data("percent"), 10), k.percentage = 0, k.canvas = a("<canvas width='" + k.options.size + "' height='" + k.options.size + "'></canvas>").get(0), k.$el.append(k.canvas), "undefined" != typeof G_vmlCanvasManager && null !== G_vmlCanvasManager && G_vmlCanvasManager.initElement(k.canvas), k.ctx = k.canvas.getContext("2d"), window.devicePixelRatio > 1.5 && (a(k.canvas).css({
                    width: k.options.size,
                    height: k.options.size
                }), k.canvas.width *= 2, k.canvas.height *= 2, k.ctx.scale(2, 2)), k.ctx.translate(k.options.size / 2, k.options.size / 2), k.$el.addClass("easyPieChart"), k.$el.css({
                    width: k.options.size,
                    height: k.options.size,
                    lineHeight: "" + k.options.size + "px"
                }), k.update(b), k
            }, this.update = function(a) {
                return k.options.animate === !1 ? f(a) : e(k.percentage, a)
            }, i = function() {
                var a, b, c;
                for (k.ctx.fillStyle = k.options.scaleColor, k.ctx.lineWidth = 1, c = [], a = b = 0; b <= 24; a = ++b) c.push(d(a));
                return c
            }, d = function(a) {
                var b;
                return b = a % 6 === 0 ? 0 : .017 * k.options.size, k.ctx.save(), k.ctx.rotate(a * Math.PI / 12), k.ctx.fillRect(k.options.size / 2 - b, 0, .05 * -k.options.size + b, 1), k.ctx.restore()
            }, j = function() {
                var a;
                return a = k.options.size / 2 - k.options.lineWidth / 2, k.options.scaleColor !== !1 && (a -= .08 * k.options.size), k.ctx.beginPath(), k.ctx.arc(0, 0, a, 0, 2 * Math.PI, !0), k.ctx.closePath(), k.ctx.strokeStyle = k.options.trackColor, k.ctx.lineWidth = k.options.lineWidth, k.ctx.stroke()
            }, h = function() {
                if (k.options.scaleColor !== !1 && i(), k.options.trackColor !== !1) return j()
            }, f = function(a) {
                var b;
                h();
                var c = k.ctx.createLinearGradient(0, 0, 170, 0);
                return c.addColorStop(0, k.options.barColor), c.addColorStop(1, k.options.barColor2), k.ctx.strokeStyle = c, k.ctx.lineCap = k.options.lineCap, k.ctx.lineWidth = k.options.lineWidth, b = k.options.size / 2 - k.options.lineWidth / 2, k.options.scaleColor !== !1 && (b -= .08 * k.options.size), k.ctx.save(), k.ctx.rotate(-Math.PI / 2), k.ctx.beginPath(), k.ctx.arc(0, 0, b, 0, 2 * Math.PI * a / 100, !1), k.ctx.stroke(), k.ctx.restore()
            }, e = function(a, b) {
                var c, d, e;
                return d = 30, e = d * k.options.animate / 1e3, c = 0, k.options.onStart.call(k), k.percentage = b, k.animation && (clearInterval(k.animation), k.animation = !1), k.animation = setInterval(function() {
                    if (k.ctx.clearRect(-k.options.size / 2, -k.options.size / 2, k.options.size, k.options.size), h.call(k), f.call(k, [g(c, a, b - a, e)]), c++, c / e > 1) return clearInterval(k.animation), k.animation = !1, k.options.onStop.call(k)
                }, 1e3 / d)
            }, g = function(a, b, c, d) {
                var e, f;
                return e = function(a) {
                    return Math.pow(a, 2)
                }, f = function(a) {
                    return a < 1 ? e(a) : 2 - e(a / 2 * -2 + 2)
                }, a /= d / 2, c / 2 * f(a) + b
            }, this.init()
        }, a.easyPieChart.defaultOptions = {
            barColor: "#ef1e25",
            barColor2: "#ef1e25",
            trackColor: "#f2f2f2",
            scaleColor: "#dfe0e0",
            lineCap: "square",
            size: 110,
            lineWidth: 12,
            animate: !1,
            onStart: a.noop,
            onStop: a.noop
        }, a.fn.easyPieChart = function(b) {
            return a.each(this, function(c, d) {
                var e;
                if (e = a(d), !e.data("easyPieChart")) return e.data("easyPieChart", new a.easyPieChart(d, b))
            })
        }
    }(jQuery)
}).call(this);