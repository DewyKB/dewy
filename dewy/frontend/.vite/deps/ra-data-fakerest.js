import {
  __commonJS,
  __toESM
} from "./chunk-ROME4SDB.js";

// node_modules/fakerest/dist/FakeRest.min.js
var require_FakeRest_min = __commonJS({
  "node_modules/fakerest/dist/FakeRest.min.js"(exports, module) {
    !function(e, t) {
      "object" == typeof exports && "object" == typeof module ? module.exports = t() : "function" == typeof define && define.amd ? define([], t) : "object" == typeof exports ? exports.FakeRest = t() : e.FakeRest = t();
    }(exports, function() {
      return function() {
        var e = { 8552: function(e2, t2, r2) {
          var n2 = r2(852)(r2(5639), "DataView");
          e2.exports = n2;
        }, 1989: function(e2, t2, r2) {
          var n2 = r2(1789), o = r2(401), i = r2(7667), u = r2(1327), a = r2(1866);
          function c(e3) {
            var t3 = -1, r3 = null == e3 ? 0 : e3.length;
            for (this.clear(); ++t3 < r3; ) {
              var n3 = e3[t3];
              this.set(n3[0], n3[1]);
            }
          }
          c.prototype.clear = n2, c.prototype.delete = o, c.prototype.get = i, c.prototype.has = u, c.prototype.set = a, e2.exports = c;
        }, 8407: function(e2, t2, r2) {
          var n2 = r2(7040), o = r2(4125), i = r2(2117), u = r2(7518), a = r2(4705);
          function c(e3) {
            var t3 = -1, r3 = null == e3 ? 0 : e3.length;
            for (this.clear(); ++t3 < r3; ) {
              var n3 = e3[t3];
              this.set(n3[0], n3[1]);
            }
          }
          c.prototype.clear = n2, c.prototype.delete = o, c.prototype.get = i, c.prototype.has = u, c.prototype.set = a, e2.exports = c;
        }, 7071: function(e2, t2, r2) {
          var n2 = r2(852)(r2(5639), "Map");
          e2.exports = n2;
        }, 3369: function(e2, t2, r2) {
          var n2 = r2(4785), o = r2(1285), i = r2(6e3), u = r2(9916), a = r2(5265);
          function c(e3) {
            var t3 = -1, r3 = null == e3 ? 0 : e3.length;
            for (this.clear(); ++t3 < r3; ) {
              var n3 = e3[t3];
              this.set(n3[0], n3[1]);
            }
          }
          c.prototype.clear = n2, c.prototype.delete = o, c.prototype.get = i, c.prototype.has = u, c.prototype.set = a, e2.exports = c;
        }, 3818: function(e2, t2, r2) {
          var n2 = r2(852)(r2(5639), "Promise");
          e2.exports = n2;
        }, 8525: function(e2, t2, r2) {
          var n2 = r2(852)(r2(5639), "Set");
          e2.exports = n2;
        }, 8668: function(e2, t2, r2) {
          var n2 = r2(3369), o = r2(619), i = r2(2385);
          function u(e3) {
            var t3 = -1, r3 = null == e3 ? 0 : e3.length;
            for (this.__data__ = new n2(); ++t3 < r3; )
              this.add(e3[t3]);
          }
          u.prototype.add = u.prototype.push = o, u.prototype.has = i, e2.exports = u;
        }, 6384: function(e2, t2, r2) {
          var n2 = r2(8407), o = r2(7465), i = r2(3779), u = r2(7599), a = r2(4758), c = r2(4309);
          function s(e3) {
            var t3 = this.__data__ = new n2(e3);
            this.size = t3.size;
          }
          s.prototype.clear = o, s.prototype.delete = i, s.prototype.get = u, s.prototype.has = a, s.prototype.set = c, e2.exports = s;
        }, 2705: function(e2, t2, r2) {
          var n2 = r2(5639).Symbol;
          e2.exports = n2;
        }, 1149: function(e2, t2, r2) {
          var n2 = r2(5639).Uint8Array;
          e2.exports = n2;
        }, 577: function(e2, t2, r2) {
          var n2 = r2(852)(r2(5639), "WeakMap");
          e2.exports = n2;
        }, 7412: function(e2) {
          e2.exports = function(e3, t2) {
            for (var r2 = -1, n2 = null == e3 ? 0 : e3.length; ++r2 < n2 && false !== t2(e3[r2], r2, e3); )
              ;
            return e3;
          };
        }, 4963: function(e2) {
          e2.exports = function(e3, t2) {
            for (var r2 = -1, n2 = null == e3 ? 0 : e3.length, o = 0, i = []; ++r2 < n2; ) {
              var u = e3[r2];
              t2(u, r2, e3) && (i[o++] = u);
            }
            return i;
          };
        }, 4636: function(e2, t2, r2) {
          var n2 = r2(2545), o = r2(5694), i = r2(1469), u = r2(4144), a = r2(5776), c = r2(6719), s = Object.prototype.hasOwnProperty;
          e2.exports = function(e3, t3) {
            var r3 = i(e3), f = !r3 && o(e3), l = !r3 && !f && u(e3), p = !r3 && !f && !l && c(e3), y = r3 || f || l || p, d = y ? n2(e3.length, String) : [], h = d.length;
            for (var v in e3)
              !t3 && !s.call(e3, v) || y && ("length" == v || l && ("offset" == v || "parent" == v) || p && ("buffer" == v || "byteLength" == v || "byteOffset" == v) || a(v, h)) || d.push(v);
            return d;
          };
        }, 9932: function(e2) {
          e2.exports = function(e3, t2) {
            for (var r2 = -1, n2 = null == e3 ? 0 : e3.length, o = Array(n2); ++r2 < n2; )
              o[r2] = t2(e3[r2], r2, e3);
            return o;
          };
        }, 2488: function(e2) {
          e2.exports = function(e3, t2) {
            for (var r2 = -1, n2 = t2.length, o = e3.length; ++r2 < n2; )
              e3[o + r2] = t2[r2];
            return e3;
          };
        }, 2908: function(e2) {
          e2.exports = function(e3, t2) {
            for (var r2 = -1, n2 = null == e3 ? 0 : e3.length; ++r2 < n2; )
              if (t2(e3[r2], r2, e3))
                return true;
            return false;
          };
        }, 4865: function(e2, t2, r2) {
          var n2 = r2(9465), o = r2(7813), i = Object.prototype.hasOwnProperty;
          e2.exports = function(e3, t3, r3) {
            var u = e3[t3];
            i.call(e3, t3) && o(u, r3) && (void 0 !== r3 || t3 in e3) || n2(e3, t3, r3);
          };
        }, 8470: function(e2, t2, r2) {
          var n2 = r2(7813);
          e2.exports = function(e3, t3) {
            for (var r3 = e3.length; r3--; )
              if (n2(e3[r3][0], t3))
                return r3;
            return -1;
          };
        }, 4037: function(e2, t2, r2) {
          var n2 = r2(8363), o = r2(3674);
          e2.exports = function(e3, t3) {
            return e3 && n2(t3, o(t3), e3);
          };
        }, 3886: function(e2, t2, r2) {
          var n2 = r2(8363), o = r2(1704);
          e2.exports = function(e3, t3) {
            return e3 && n2(t3, o(t3), e3);
          };
        }, 9465: function(e2, t2, r2) {
          var n2 = r2(8777);
          e2.exports = function(e3, t3, r3) {
            "__proto__" == t3 && n2 ? n2(e3, t3, { configurable: true, enumerable: true, value: r3, writable: true }) : e3[t3] = r3;
          };
        }, 5990: function(e2, t2, r2) {
          var n2 = r2(6384), o = r2(7412), i = r2(4865), u = r2(4037), a = r2(3886), c = r2(4626), s = r2(278), f = r2(8805), l = r2(1911), p = r2(8234), y = r2(6904), d = r2(4160), h = r2(3824), v = r2(9148), b = r2(8517), g = r2(1469), m = r2(4144), j = r2(6688), x = r2(3218), _ = r2(2928), O = r2(3674), w = r2(1704), A = "[object Arguments]", S = "[object Function]", E = "[object Object]", k = {};
          k[A] = k["[object Array]"] = k["[object ArrayBuffer]"] = k["[object DataView]"] = k["[object Boolean]"] = k["[object Date]"] = k["[object Float32Array]"] = k["[object Float64Array]"] = k["[object Int8Array]"] = k["[object Int16Array]"] = k["[object Int32Array]"] = k["[object Map]"] = k["[object Number]"] = k[E] = k["[object RegExp]"] = k["[object Set]"] = k["[object String]"] = k["[object Symbol]"] = k["[object Uint8Array]"] = k["[object Uint8ClampedArray]"] = k["[object Uint16Array]"] = k["[object Uint32Array]"] = true, k["[object Error]"] = k[S] = k["[object WeakMap]"] = false, e2.exports = function e3(t3, r3, C, T, P, q) {
            var I, U = 1 & r3, R = 2 & r3, N = 4 & r3;
            if (C && (I = P ? C(t3, T, P, q) : C(t3)), void 0 !== I)
              return I;
            if (!x(t3))
              return t3;
            var $ = g(t3);
            if ($) {
              if (I = h(t3), !U)
                return s(t3, I);
            } else {
              var z = d(t3), F = z == S || "[object GeneratorFunction]" == z;
              if (m(t3))
                return c(t3, U);
              if (z == E || z == A || F && !P) {
                if (I = R || F ? {} : b(t3), !U)
                  return R ? l(t3, a(I, t3)) : f(t3, u(I, t3));
              } else {
                if (!k[z])
                  return P ? t3 : {};
                I = v(t3, z, U);
              }
            }
            q || (q = new n2());
            var M = q.get(t3);
            if (M)
              return M;
            q.set(t3, I), _(t3) ? t3.forEach(function(n3) {
              I.add(e3(n3, r3, C, n3, t3, q));
            }) : j(t3) && t3.forEach(function(n3, o2) {
              I.set(o2, e3(n3, r3, C, o2, t3, q));
            });
            var B = $ ? void 0 : (N ? R ? y : p : R ? w : O)(t3);
            return o(B || t3, function(n3, o2) {
              B && (n3 = t3[o2 = n3]), i(I, o2, e3(n3, r3, C, o2, t3, q));
            }), I;
          };
        }, 3118: function(e2, t2, r2) {
          var n2 = r2(3218), o = Object.create, i = function() {
            function e3() {
            }
            return function(t3) {
              if (!n2(t3))
                return {};
              if (o)
                return o(t3);
              e3.prototype = t3;
              var r3 = new e3();
              return e3.prototype = void 0, r3;
            };
          }();
          e2.exports = i;
        }, 7786: function(e2, t2, r2) {
          var n2 = r2(1811), o = r2(327);
          e2.exports = function(e3, t3) {
            for (var r3 = 0, i = (t3 = n2(t3, e3)).length; null != e3 && r3 < i; )
              e3 = e3[o(t3[r3++])];
            return r3 && r3 == i ? e3 : void 0;
          };
        }, 8866: function(e2, t2, r2) {
          var n2 = r2(2488), o = r2(1469);
          e2.exports = function(e3, t3, r3) {
            var i = t3(e3);
            return o(e3) ? i : n2(i, r3(e3));
          };
        }, 4239: function(e2, t2, r2) {
          var n2 = r2(2705), o = r2(9607), i = r2(2333), u = n2 ? n2.toStringTag : void 0;
          e2.exports = function(e3) {
            return null == e3 ? void 0 === e3 ? "[object Undefined]" : "[object Null]" : u && u in Object(e3) ? o(e3) : i(e3);
          };
        }, 9454: function(e2, t2, r2) {
          var n2 = r2(4239), o = r2(7005);
          e2.exports = function(e3) {
            return o(e3) && "[object Arguments]" == n2(e3);
          };
        }, 939: function(e2, t2, r2) {
          var n2 = r2(2492), o = r2(7005);
          e2.exports = function e3(t3, r3, i, u, a) {
            return t3 === r3 || (null == t3 || null == r3 || !o(t3) && !o(r3) ? t3 != t3 && r3 != r3 : n2(t3, r3, i, u, e3, a));
          };
        }, 2492: function(e2, t2, r2) {
          var n2 = r2(6384), o = r2(7114), i = r2(8351), u = r2(6096), a = r2(4160), c = r2(1469), s = r2(4144), f = r2(6719), l = "[object Arguments]", p = "[object Array]", y = "[object Object]", d = Object.prototype.hasOwnProperty;
          e2.exports = function(e3, t3, r3, h, v, b) {
            var g = c(e3), m = c(t3), j = g ? p : a(e3), x = m ? p : a(t3), _ = (j = j == l ? y : j) == y, O = (x = x == l ? y : x) == y, w = j == x;
            if (w && s(e3)) {
              if (!s(t3))
                return false;
              g = true, _ = false;
            }
            if (w && !_)
              return b || (b = new n2()), g || f(e3) ? o(e3, t3, r3, h, v, b) : i(e3, t3, j, r3, h, v, b);
            if (!(1 & r3)) {
              var A = _ && d.call(e3, "__wrapped__"), S = O && d.call(t3, "__wrapped__");
              if (A || S) {
                var E = A ? e3.value() : e3, k = S ? t3.value() : t3;
                return b || (b = new n2()), v(E, k, r3, h, b);
              }
            }
            return !!w && (b || (b = new n2()), u(e3, t3, r3, h, v, b));
          };
        }, 5588: function(e2, t2, r2) {
          var n2 = r2(4160), o = r2(7005);
          e2.exports = function(e3) {
            return o(e3) && "[object Map]" == n2(e3);
          };
        }, 2958: function(e2, t2, r2) {
          var n2 = r2(6384), o = r2(939);
          e2.exports = function(e3, t3, r3, i) {
            var u = r3.length, a = u, c = !i;
            if (null == e3)
              return !a;
            for (e3 = Object(e3); u--; ) {
              var s = r3[u];
              if (c && s[2] ? s[1] !== e3[s[0]] : !(s[0] in e3))
                return false;
            }
            for (; ++u < a; ) {
              var f = (s = r3[u])[0], l = e3[f], p = s[1];
              if (c && s[2]) {
                if (void 0 === l && !(f in e3))
                  return false;
              } else {
                var y = new n2();
                if (i)
                  var d = i(l, p, f, e3, t3, y);
                if (!(void 0 === d ? o(p, l, 3, i, y) : d))
                  return false;
              }
            }
            return true;
          };
        }, 8458: function(e2, t2, r2) {
          var n2 = r2(3560), o = r2(5346), i = r2(3218), u = r2(346), a = /^\[object .+?Constructor\]$/, c = Function.prototype, s = Object.prototype, f = c.toString, l = s.hasOwnProperty, p = RegExp("^" + f.call(l).replace(/[\\^$.*+?()[\]{}|]/g, "\\$&").replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g, "$1.*?") + "$");
          e2.exports = function(e3) {
            return !(!i(e3) || o(e3)) && (n2(e3) ? p : a).test(u(e3));
          };
        }, 9221: function(e2, t2, r2) {
          var n2 = r2(4160), o = r2(7005);
          e2.exports = function(e3) {
            return o(e3) && "[object Set]" == n2(e3);
          };
        }, 8749: function(e2, t2, r2) {
          var n2 = r2(4239), o = r2(1780), i = r2(7005), u = {};
          u["[object Float32Array]"] = u["[object Float64Array]"] = u["[object Int8Array]"] = u["[object Int16Array]"] = u["[object Int32Array]"] = u["[object Uint8Array]"] = u["[object Uint8ClampedArray]"] = u["[object Uint16Array]"] = u["[object Uint32Array]"] = true, u["[object Arguments]"] = u["[object Array]"] = u["[object ArrayBuffer]"] = u["[object Boolean]"] = u["[object DataView]"] = u["[object Date]"] = u["[object Error]"] = u["[object Function]"] = u["[object Map]"] = u["[object Number]"] = u["[object Object]"] = u["[object RegExp]"] = u["[object Set]"] = u["[object String]"] = u["[object WeakMap]"] = false, e2.exports = function(e3) {
            return i(e3) && o(e3.length) && !!u[n2(e3)];
          };
        }, 280: function(e2, t2, r2) {
          var n2 = r2(5726), o = r2(6916), i = Object.prototype.hasOwnProperty;
          e2.exports = function(e3) {
            if (!n2(e3))
              return o(e3);
            var t3 = [];
            for (var r3 in Object(e3))
              i.call(e3, r3) && "constructor" != r3 && t3.push(r3);
            return t3;
          };
        }, 313: function(e2, t2, r2) {
          var n2 = r2(3218), o = r2(5726), i = r2(3498), u = Object.prototype.hasOwnProperty;
          e2.exports = function(e3) {
            if (!n2(e3))
              return i(e3);
            var t3 = o(e3), r3 = [];
            for (var a in e3)
              ("constructor" != a || !t3 && u.call(e3, a)) && r3.push(a);
            return r3;
          };
        }, 1573: function(e2, t2, r2) {
          var n2 = r2(2958), o = r2(1499), i = r2(2634);
          e2.exports = function(e3) {
            var t3 = o(e3);
            return 1 == t3.length && t3[0][2] ? i(t3[0][0], t3[0][1]) : function(r3) {
              return r3 === e3 || n2(r3, e3, t3);
            };
          };
        }, 2545: function(e2) {
          e2.exports = function(e3, t2) {
            for (var r2 = -1, n2 = Array(e3); ++r2 < e3; )
              n2[r2] = t2(r2);
            return n2;
          };
        }, 531: function(e2, t2, r2) {
          var n2 = r2(2705), o = r2(9932), i = r2(1469), u = r2(3448), a = n2 ? n2.prototype : void 0, c = a ? a.toString : void 0;
          e2.exports = function e3(t3) {
            if ("string" == typeof t3)
              return t3;
            if (i(t3))
              return o(t3, e3) + "";
            if (u(t3))
              return c ? c.call(t3) : "";
            var r3 = t3 + "";
            return "0" == r3 && 1 / t3 == -Infinity ? "-0" : r3;
          };
        }, 1717: function(e2) {
          e2.exports = function(e3) {
            return function(t2) {
              return e3(t2);
            };
          };
        }, 4757: function(e2) {
          e2.exports = function(e3, t2) {
            return e3.has(t2);
          };
        }, 1811: function(e2, t2, r2) {
          var n2 = r2(1469), o = r2(5403), i = r2(5514), u = r2(9833);
          e2.exports = function(e3, t3) {
            return n2(e3) ? e3 : o(e3, t3) ? [e3] : i(u(e3));
          };
        }, 4318: function(e2, t2, r2) {
          var n2 = r2(1149);
          e2.exports = function(e3) {
            var t3 = new e3.constructor(e3.byteLength);
            return new n2(t3).set(new n2(e3)), t3;
          };
        }, 4626: function(e2, t2, r2) {
          e2 = r2.nmd(e2);
          var n2 = r2(5639), o = t2 && !t2.nodeType && t2, i = o && e2 && !e2.nodeType && e2, u = i && i.exports === o ? n2.Buffer : void 0, a = u ? u.allocUnsafe : void 0;
          e2.exports = function(e3, t3) {
            if (t3)
              return e3.slice();
            var r3 = e3.length, n3 = a ? a(r3) : new e3.constructor(r3);
            return e3.copy(n3), n3;
          };
        }, 7157: function(e2, t2, r2) {
          var n2 = r2(4318);
          e2.exports = function(e3, t3) {
            var r3 = t3 ? n2(e3.buffer) : e3.buffer;
            return new e3.constructor(r3, e3.byteOffset, e3.byteLength);
          };
        }, 3147: function(e2) {
          var t2 = /\w*$/;
          e2.exports = function(e3) {
            var r2 = new e3.constructor(e3.source, t2.exec(e3));
            return r2.lastIndex = e3.lastIndex, r2;
          };
        }, 419: function(e2, t2, r2) {
          var n2 = r2(2705), o = n2 ? n2.prototype : void 0, i = o ? o.valueOf : void 0;
          e2.exports = function(e3) {
            return i ? Object(i.call(e3)) : {};
          };
        }, 7133: function(e2, t2, r2) {
          var n2 = r2(4318);
          e2.exports = function(e3, t3) {
            var r3 = t3 ? n2(e3.buffer) : e3.buffer;
            return new e3.constructor(r3, e3.byteOffset, e3.length);
          };
        }, 278: function(e2) {
          e2.exports = function(e3, t2) {
            var r2 = -1, n2 = e3.length;
            for (t2 || (t2 = Array(n2)); ++r2 < n2; )
              t2[r2] = e3[r2];
            return t2;
          };
        }, 8363: function(e2, t2, r2) {
          var n2 = r2(4865), o = r2(9465);
          e2.exports = function(e3, t3, r3, i) {
            var u = !r3;
            r3 || (r3 = {});
            for (var a = -1, c = t3.length; ++a < c; ) {
              var s = t3[a], f = i ? i(r3[s], e3[s], s, r3, e3) : void 0;
              void 0 === f && (f = e3[s]), u ? o(r3, s, f) : n2(r3, s, f);
            }
            return r3;
          };
        }, 8805: function(e2, t2, r2) {
          var n2 = r2(8363), o = r2(9551);
          e2.exports = function(e3, t3) {
            return n2(e3, o(e3), t3);
          };
        }, 1911: function(e2, t2, r2) {
          var n2 = r2(8363), o = r2(1442);
          e2.exports = function(e3, t3) {
            return n2(e3, o(e3), t3);
          };
        }, 4429: function(e2, t2, r2) {
          var n2 = r2(5639)["__core-js_shared__"];
          e2.exports = n2;
        }, 8777: function(e2, t2, r2) {
          var n2 = r2(852), o = function() {
            try {
              var e3 = n2(Object, "defineProperty");
              return e3({}, "", {}), e3;
            } catch (e4) {
            }
          }();
          e2.exports = o;
        }, 7114: function(e2, t2, r2) {
          var n2 = r2(8668), o = r2(2908), i = r2(4757);
          e2.exports = function(e3, t3, r3, u, a, c) {
            var s = 1 & r3, f = e3.length, l = t3.length;
            if (f != l && !(s && l > f))
              return false;
            var p = c.get(e3), y = c.get(t3);
            if (p && y)
              return p == t3 && y == e3;
            var d = -1, h = true, v = 2 & r3 ? new n2() : void 0;
            for (c.set(e3, t3), c.set(t3, e3); ++d < f; ) {
              var b = e3[d], g = t3[d];
              if (u)
                var m = s ? u(g, b, d, t3, e3, c) : u(b, g, d, e3, t3, c);
              if (void 0 !== m) {
                if (m)
                  continue;
                h = false;
                break;
              }
              if (v) {
                if (!o(t3, function(e4, t4) {
                  if (!i(v, t4) && (b === e4 || a(b, e4, r3, u, c)))
                    return v.push(t4);
                })) {
                  h = false;
                  break;
                }
              } else if (b !== g && !a(b, g, r3, u, c)) {
                h = false;
                break;
              }
            }
            return c.delete(e3), c.delete(t3), h;
          };
        }, 8351: function(e2, t2, r2) {
          var n2 = r2(2705), o = r2(1149), i = r2(7813), u = r2(7114), a = r2(8776), c = r2(1814), s = n2 ? n2.prototype : void 0, f = s ? s.valueOf : void 0;
          e2.exports = function(e3, t3, r3, n3, s2, l, p) {
            switch (r3) {
              case "[object DataView]":
                if (e3.byteLength != t3.byteLength || e3.byteOffset != t3.byteOffset)
                  return false;
                e3 = e3.buffer, t3 = t3.buffer;
              case "[object ArrayBuffer]":
                return !(e3.byteLength != t3.byteLength || !l(new o(e3), new o(t3)));
              case "[object Boolean]":
              case "[object Date]":
              case "[object Number]":
                return i(+e3, +t3);
              case "[object Error]":
                return e3.name == t3.name && e3.message == t3.message;
              case "[object RegExp]":
              case "[object String]":
                return e3 == t3 + "";
              case "[object Map]":
                var y = a;
              case "[object Set]":
                var d = 1 & n3;
                if (y || (y = c), e3.size != t3.size && !d)
                  return false;
                var h = p.get(e3);
                if (h)
                  return h == t3;
                n3 |= 2, p.set(e3, t3);
                var v = u(y(e3), y(t3), n3, s2, l, p);
                return p.delete(e3), v;
              case "[object Symbol]":
                if (f)
                  return f.call(e3) == f.call(t3);
            }
            return false;
          };
        }, 6096: function(e2, t2, r2) {
          var n2 = r2(8234), o = Object.prototype.hasOwnProperty;
          e2.exports = function(e3, t3, r3, i, u, a) {
            var c = 1 & r3, s = n2(e3), f = s.length;
            if (f != n2(t3).length && !c)
              return false;
            for (var l = f; l--; ) {
              var p = s[l];
              if (!(c ? p in t3 : o.call(t3, p)))
                return false;
            }
            var y = a.get(e3), d = a.get(t3);
            if (y && d)
              return y == t3 && d == e3;
            var h = true;
            a.set(e3, t3), a.set(t3, e3);
            for (var v = c; ++l < f; ) {
              var b = e3[p = s[l]], g = t3[p];
              if (i)
                var m = c ? i(g, b, p, t3, e3, a) : i(b, g, p, e3, t3, a);
              if (!(void 0 === m ? b === g || u(b, g, r3, i, a) : m)) {
                h = false;
                break;
              }
              v || (v = "constructor" == p);
            }
            if (h && !v) {
              var j = e3.constructor, x = t3.constructor;
              j == x || !("constructor" in e3) || !("constructor" in t3) || "function" == typeof j && j instanceof j && "function" == typeof x && x instanceof x || (h = false);
            }
            return a.delete(e3), a.delete(t3), h;
          };
        }, 1957: function(e2, t2, r2) {
          var n2 = "object" == typeof r2.g && r2.g && r2.g.Object === Object && r2.g;
          e2.exports = n2;
        }, 8234: function(e2, t2, r2) {
          var n2 = r2(8866), o = r2(9551), i = r2(3674);
          e2.exports = function(e3) {
            return n2(e3, i, o);
          };
        }, 6904: function(e2, t2, r2) {
          var n2 = r2(8866), o = r2(1442), i = r2(1704);
          e2.exports = function(e3) {
            return n2(e3, i, o);
          };
        }, 5050: function(e2, t2, r2) {
          var n2 = r2(7019);
          e2.exports = function(e3, t3) {
            var r3 = e3.__data__;
            return n2(t3) ? r3["string" == typeof t3 ? "string" : "hash"] : r3.map;
          };
        }, 1499: function(e2, t2, r2) {
          var n2 = r2(9162), o = r2(3674);
          e2.exports = function(e3) {
            for (var t3 = o(e3), r3 = t3.length; r3--; ) {
              var i = t3[r3], u = e3[i];
              t3[r3] = [i, u, n2(u)];
            }
            return t3;
          };
        }, 852: function(e2, t2, r2) {
          var n2 = r2(8458), o = r2(7801);
          e2.exports = function(e3, t3) {
            var r3 = o(e3, t3);
            return n2(r3) ? r3 : void 0;
          };
        }, 5924: function(e2, t2, r2) {
          var n2 = r2(5569)(Object.getPrototypeOf, Object);
          e2.exports = n2;
        }, 9607: function(e2, t2, r2) {
          var n2 = r2(2705), o = Object.prototype, i = o.hasOwnProperty, u = o.toString, a = n2 ? n2.toStringTag : void 0;
          e2.exports = function(e3) {
            var t3 = i.call(e3, a), r3 = e3[a];
            try {
              e3[a] = void 0;
              var n3 = true;
            } catch (e4) {
            }
            var o2 = u.call(e3);
            return n3 && (t3 ? e3[a] = r3 : delete e3[a]), o2;
          };
        }, 9551: function(e2, t2, r2) {
          var n2 = r2(4963), o = r2(479), i = Object.prototype.propertyIsEnumerable, u = Object.getOwnPropertySymbols, a = u ? function(e3) {
            return null == e3 ? [] : (e3 = Object(e3), n2(u(e3), function(t3) {
              return i.call(e3, t3);
            }));
          } : o;
          e2.exports = a;
        }, 1442: function(e2, t2, r2) {
          var n2 = r2(2488), o = r2(5924), i = r2(9551), u = r2(479), a = Object.getOwnPropertySymbols ? function(e3) {
            for (var t3 = []; e3; )
              n2(t3, i(e3)), e3 = o(e3);
            return t3;
          } : u;
          e2.exports = a;
        }, 4160: function(e2, t2, r2) {
          var n2 = r2(8552), o = r2(7071), i = r2(3818), u = r2(8525), a = r2(577), c = r2(4239), s = r2(346), f = "[object Map]", l = "[object Promise]", p = "[object Set]", y = "[object WeakMap]", d = "[object DataView]", h = s(n2), v = s(o), b = s(i), g = s(u), m = s(a), j = c;
          (n2 && j(new n2(new ArrayBuffer(1))) != d || o && j(new o()) != f || i && j(i.resolve()) != l || u && j(new u()) != p || a && j(new a()) != y) && (j = function(e3) {
            var t3 = c(e3), r3 = "[object Object]" == t3 ? e3.constructor : void 0, n3 = r3 ? s(r3) : "";
            if (n3)
              switch (n3) {
                case h:
                  return d;
                case v:
                  return f;
                case b:
                  return l;
                case g:
                  return p;
                case m:
                  return y;
              }
            return t3;
          }), e2.exports = j;
        }, 7801: function(e2) {
          e2.exports = function(e3, t2) {
            return null == e3 ? void 0 : e3[t2];
          };
        }, 1789: function(e2, t2, r2) {
          var n2 = r2(4536);
          e2.exports = function() {
            this.__data__ = n2 ? n2(null) : {}, this.size = 0;
          };
        }, 401: function(e2) {
          e2.exports = function(e3) {
            var t2 = this.has(e3) && delete this.__data__[e3];
            return this.size -= t2 ? 1 : 0, t2;
          };
        }, 7667: function(e2, t2, r2) {
          var n2 = r2(4536), o = Object.prototype.hasOwnProperty;
          e2.exports = function(e3) {
            var t3 = this.__data__;
            if (n2) {
              var r3 = t3[e3];
              return "__lodash_hash_undefined__" === r3 ? void 0 : r3;
            }
            return o.call(t3, e3) ? t3[e3] : void 0;
          };
        }, 1327: function(e2, t2, r2) {
          var n2 = r2(4536), o = Object.prototype.hasOwnProperty;
          e2.exports = function(e3) {
            var t3 = this.__data__;
            return n2 ? void 0 !== t3[e3] : o.call(t3, e3);
          };
        }, 1866: function(e2, t2, r2) {
          var n2 = r2(4536);
          e2.exports = function(e3, t3) {
            var r3 = this.__data__;
            return this.size += this.has(e3) ? 0 : 1, r3[e3] = n2 && void 0 === t3 ? "__lodash_hash_undefined__" : t3, this;
          };
        }, 3824: function(e2) {
          var t2 = Object.prototype.hasOwnProperty;
          e2.exports = function(e3) {
            var r2 = e3.length, n2 = new e3.constructor(r2);
            return r2 && "string" == typeof e3[0] && t2.call(e3, "index") && (n2.index = e3.index, n2.input = e3.input), n2;
          };
        }, 9148: function(e2, t2, r2) {
          var n2 = r2(4318), o = r2(7157), i = r2(3147), u = r2(419), a = r2(7133);
          e2.exports = function(e3, t3, r3) {
            var c = e3.constructor;
            switch (t3) {
              case "[object ArrayBuffer]":
                return n2(e3);
              case "[object Boolean]":
              case "[object Date]":
                return new c(+e3);
              case "[object DataView]":
                return o(e3, r3);
              case "[object Float32Array]":
              case "[object Float64Array]":
              case "[object Int8Array]":
              case "[object Int16Array]":
              case "[object Int32Array]":
              case "[object Uint8Array]":
              case "[object Uint8ClampedArray]":
              case "[object Uint16Array]":
              case "[object Uint32Array]":
                return a(e3, r3);
              case "[object Map]":
              case "[object Set]":
                return new c();
              case "[object Number]":
              case "[object String]":
                return new c(e3);
              case "[object RegExp]":
                return i(e3);
              case "[object Symbol]":
                return u(e3);
            }
          };
        }, 8517: function(e2, t2, r2) {
          var n2 = r2(3118), o = r2(5924), i = r2(5726);
          e2.exports = function(e3) {
            return "function" != typeof e3.constructor || i(e3) ? {} : n2(o(e3));
          };
        }, 5776: function(e2) {
          var t2 = /^(?:0|[1-9]\d*)$/;
          e2.exports = function(e3, r2) {
            var n2 = typeof e3;
            return !!(r2 = null == r2 ? 9007199254740991 : r2) && ("number" == n2 || "symbol" != n2 && t2.test(e3)) && e3 > -1 && e3 % 1 == 0 && e3 < r2;
          };
        }, 5403: function(e2, t2, r2) {
          var n2 = r2(1469), o = r2(3448), i = /\.|\[(?:[^[\]]*|(["'])(?:(?!\1)[^\\]|\\.)*?\1)\]/, u = /^\w*$/;
          e2.exports = function(e3, t3) {
            if (n2(e3))
              return false;
            var r3 = typeof e3;
            return !("number" != r3 && "symbol" != r3 && "boolean" != r3 && null != e3 && !o(e3)) || (u.test(e3) || !i.test(e3) || null != t3 && e3 in Object(t3));
          };
        }, 7019: function(e2) {
          e2.exports = function(e3) {
            var t2 = typeof e3;
            return "string" == t2 || "number" == t2 || "symbol" == t2 || "boolean" == t2 ? "__proto__" !== e3 : null === e3;
          };
        }, 5346: function(e2, t2, r2) {
          var n2, o = r2(4429), i = (n2 = /[^.]+$/.exec(o && o.keys && o.keys.IE_PROTO || "")) ? "Symbol(src)_1." + n2 : "";
          e2.exports = function(e3) {
            return !!i && i in e3;
          };
        }, 5726: function(e2) {
          var t2 = Object.prototype;
          e2.exports = function(e3) {
            var r2 = e3 && e3.constructor;
            return e3 === ("function" == typeof r2 && r2.prototype || t2);
          };
        }, 9162: function(e2, t2, r2) {
          var n2 = r2(3218);
          e2.exports = function(e3) {
            return e3 == e3 && !n2(e3);
          };
        }, 7040: function(e2) {
          e2.exports = function() {
            this.__data__ = [], this.size = 0;
          };
        }, 4125: function(e2, t2, r2) {
          var n2 = r2(8470), o = Array.prototype.splice;
          e2.exports = function(e3) {
            var t3 = this.__data__, r3 = n2(t3, e3);
            return !(r3 < 0) && (r3 == t3.length - 1 ? t3.pop() : o.call(t3, r3, 1), --this.size, true);
          };
        }, 2117: function(e2, t2, r2) {
          var n2 = r2(8470);
          e2.exports = function(e3) {
            var t3 = this.__data__, r3 = n2(t3, e3);
            return r3 < 0 ? void 0 : t3[r3][1];
          };
        }, 7518: function(e2, t2, r2) {
          var n2 = r2(8470);
          e2.exports = function(e3) {
            return n2(this.__data__, e3) > -1;
          };
        }, 4705: function(e2, t2, r2) {
          var n2 = r2(8470);
          e2.exports = function(e3, t3) {
            var r3 = this.__data__, o = n2(r3, e3);
            return o < 0 ? (++this.size, r3.push([e3, t3])) : r3[o][1] = t3, this;
          };
        }, 4785: function(e2, t2, r2) {
          var n2 = r2(1989), o = r2(8407), i = r2(7071);
          e2.exports = function() {
            this.size = 0, this.__data__ = { hash: new n2(), map: new (i || o)(), string: new n2() };
          };
        }, 1285: function(e2, t2, r2) {
          var n2 = r2(5050);
          e2.exports = function(e3) {
            var t3 = n2(this, e3).delete(e3);
            return this.size -= t3 ? 1 : 0, t3;
          };
        }, 6e3: function(e2, t2, r2) {
          var n2 = r2(5050);
          e2.exports = function(e3) {
            return n2(this, e3).get(e3);
          };
        }, 9916: function(e2, t2, r2) {
          var n2 = r2(5050);
          e2.exports = function(e3) {
            return n2(this, e3).has(e3);
          };
        }, 5265: function(e2, t2, r2) {
          var n2 = r2(5050);
          e2.exports = function(e3, t3) {
            var r3 = n2(this, e3), o = r3.size;
            return r3.set(e3, t3), this.size += r3.size == o ? 0 : 1, this;
          };
        }, 8776: function(e2) {
          e2.exports = function(e3) {
            var t2 = -1, r2 = Array(e3.size);
            return e3.forEach(function(e4, n2) {
              r2[++t2] = [n2, e4];
            }), r2;
          };
        }, 2634: function(e2) {
          e2.exports = function(e3, t2) {
            return function(r2) {
              return null != r2 && (r2[e3] === t2 && (void 0 !== t2 || e3 in Object(r2)));
            };
          };
        }, 4523: function(e2, t2, r2) {
          var n2 = r2(8306);
          e2.exports = function(e3) {
            var t3 = n2(e3, function(e4) {
              return 500 === r3.size && r3.clear(), e4;
            }), r3 = t3.cache;
            return t3;
          };
        }, 4536: function(e2, t2, r2) {
          var n2 = r2(852)(Object, "create");
          e2.exports = n2;
        }, 6916: function(e2, t2, r2) {
          var n2 = r2(5569)(Object.keys, Object);
          e2.exports = n2;
        }, 3498: function(e2) {
          e2.exports = function(e3) {
            var t2 = [];
            if (null != e3)
              for (var r2 in Object(e3))
                t2.push(r2);
            return t2;
          };
        }, 1167: function(e2, t2, r2) {
          e2 = r2.nmd(e2);
          var n2 = r2(1957), o = t2 && !t2.nodeType && t2, i = o && e2 && !e2.nodeType && e2, u = i && i.exports === o && n2.process, a = function() {
            try {
              var e3 = i && i.require && i.require("util").types;
              return e3 || u && u.binding && u.binding("util");
            } catch (e4) {
            }
          }();
          e2.exports = a;
        }, 2333: function(e2) {
          var t2 = Object.prototype.toString;
          e2.exports = function(e3) {
            return t2.call(e3);
          };
        }, 5569: function(e2) {
          e2.exports = function(e3, t2) {
            return function(r2) {
              return e3(t2(r2));
            };
          };
        }, 5639: function(e2, t2, r2) {
          var n2 = r2(1957), o = "object" == typeof self && self && self.Object === Object && self, i = n2 || o || Function("return this")();
          e2.exports = i;
        }, 619: function(e2) {
          e2.exports = function(e3) {
            return this.__data__.set(e3, "__lodash_hash_undefined__"), this;
          };
        }, 2385: function(e2) {
          e2.exports = function(e3) {
            return this.__data__.has(e3);
          };
        }, 1814: function(e2) {
          e2.exports = function(e3) {
            var t2 = -1, r2 = Array(e3.size);
            return e3.forEach(function(e4) {
              r2[++t2] = e4;
            }), r2;
          };
        }, 7465: function(e2, t2, r2) {
          var n2 = r2(8407);
          e2.exports = function() {
            this.__data__ = new n2(), this.size = 0;
          };
        }, 3779: function(e2) {
          e2.exports = function(e3) {
            var t2 = this.__data__, r2 = t2.delete(e3);
            return this.size = t2.size, r2;
          };
        }, 7599: function(e2) {
          e2.exports = function(e3) {
            return this.__data__.get(e3);
          };
        }, 4758: function(e2) {
          e2.exports = function(e3) {
            return this.__data__.has(e3);
          };
        }, 4309: function(e2, t2, r2) {
          var n2 = r2(8407), o = r2(7071), i = r2(3369);
          e2.exports = function(e3, t3) {
            var r3 = this.__data__;
            if (r3 instanceof n2) {
              var u = r3.__data__;
              if (!o || u.length < 199)
                return u.push([e3, t3]), this.size = ++r3.size, this;
              r3 = this.__data__ = new i(u);
            }
            return r3.set(e3, t3), this.size = r3.size, this;
          };
        }, 5514: function(e2, t2, r2) {
          var n2 = r2(4523), o = /[^.[\]]+|\[(?:(-?\d+(?:\.\d+)?)|(["'])((?:(?!\2)[^\\]|\\.)*?)\2)\]|(?=(?:\.|\[\])(?:\.|\[\]|$))/g, i = /\\(\\)?/g, u = n2(function(e3) {
            var t3 = [];
            return 46 === e3.charCodeAt(0) && t3.push(""), e3.replace(o, function(e4, r3, n3, o2) {
              t3.push(n3 ? o2.replace(i, "$1") : r3 || e4);
            }), t3;
          });
          e2.exports = u;
        }, 327: function(e2, t2, r2) {
          var n2 = r2(3448);
          e2.exports = function(e3) {
            if ("string" == typeof e3 || n2(e3))
              return e3;
            var t3 = e3 + "";
            return "0" == t3 && 1 / e3 == -Infinity ? "-0" : t3;
          };
        }, 346: function(e2) {
          var t2 = Function.prototype.toString;
          e2.exports = function(e3) {
            if (null != e3) {
              try {
                return t2.call(e3);
              } catch (e4) {
              }
              try {
                return e3 + "";
              } catch (e4) {
              }
            }
            return "";
          };
        }, 7813: function(e2) {
          e2.exports = function(e3, t2) {
            return e3 === t2 || e3 != e3 && t2 != t2;
          };
        }, 7361: function(e2, t2, r2) {
          var n2 = r2(7786);
          e2.exports = function(e3, t3, r3) {
            var o = null == e3 ? void 0 : n2(e3, t3);
            return void 0 === o ? r3 : o;
          };
        }, 5694: function(e2, t2, r2) {
          var n2 = r2(9454), o = r2(7005), i = Object.prototype, u = i.hasOwnProperty, a = i.propertyIsEnumerable, c = n2(function() {
            return arguments;
          }()) ? n2 : function(e3) {
            return o(e3) && u.call(e3, "callee") && !a.call(e3, "callee");
          };
          e2.exports = c;
        }, 1469: function(e2) {
          var t2 = Array.isArray;
          e2.exports = t2;
        }, 8612: function(e2, t2, r2) {
          var n2 = r2(3560), o = r2(1780);
          e2.exports = function(e3) {
            return null != e3 && o(e3.length) && !n2(e3);
          };
        }, 4144: function(e2, t2, r2) {
          e2 = r2.nmd(e2);
          var n2 = r2(5639), o = r2(5062), i = t2 && !t2.nodeType && t2, u = i && e2 && !e2.nodeType && e2, a = u && u.exports === i ? n2.Buffer : void 0, c = (a ? a.isBuffer : void 0) || o;
          e2.exports = c;
        }, 3560: function(e2, t2, r2) {
          var n2 = r2(4239), o = r2(3218);
          e2.exports = function(e3) {
            if (!o(e3))
              return false;
            var t3 = n2(e3);
            return "[object Function]" == t3 || "[object GeneratorFunction]" == t3 || "[object AsyncFunction]" == t3 || "[object Proxy]" == t3;
          };
        }, 1780: function(e2) {
          e2.exports = function(e3) {
            return "number" == typeof e3 && e3 > -1 && e3 % 1 == 0 && e3 <= 9007199254740991;
          };
        }, 6688: function(e2, t2, r2) {
          var n2 = r2(5588), o = r2(1717), i = r2(1167), u = i && i.isMap, a = u ? o(u) : n2;
          e2.exports = a;
        }, 3218: function(e2) {
          e2.exports = function(e3) {
            var t2 = typeof e3;
            return null != e3 && ("object" == t2 || "function" == t2);
          };
        }, 7005: function(e2) {
          e2.exports = function(e3) {
            return null != e3 && "object" == typeof e3;
          };
        }, 2928: function(e2, t2, r2) {
          var n2 = r2(9221), o = r2(1717), i = r2(1167), u = i && i.isSet, a = u ? o(u) : n2;
          e2.exports = a;
        }, 3448: function(e2, t2, r2) {
          var n2 = r2(4239), o = r2(7005);
          e2.exports = function(e3) {
            return "symbol" == typeof e3 || o(e3) && "[object Symbol]" == n2(e3);
          };
        }, 6719: function(e2, t2, r2) {
          var n2 = r2(8749), o = r2(1717), i = r2(1167), u = i && i.isTypedArray, a = u ? o(u) : n2;
          e2.exports = a;
        }, 3674: function(e2, t2, r2) {
          var n2 = r2(4636), o = r2(280), i = r2(8612);
          e2.exports = function(e3) {
            return i(e3) ? n2(e3) : o(e3);
          };
        }, 1704: function(e2, t2, r2) {
          var n2 = r2(4636), o = r2(313), i = r2(8612);
          e2.exports = function(e3) {
            return i(e3) ? n2(e3, true) : o(e3);
          };
        }, 6410: function(e2, t2, r2) {
          var n2 = r2(5990), o = r2(1573);
          e2.exports = function(e3) {
            return o(n2(e3, 1));
          };
        }, 8306: function(e2, t2, r2) {
          var n2 = r2(3369);
          function o(e3, t3) {
            if ("function" != typeof e3 || null != t3 && "function" != typeof t3)
              throw new TypeError("Expected a function");
            var r3 = function() {
              var n3 = arguments, o2 = t3 ? t3.apply(this, n3) : n3[0], i = r3.cache;
              if (i.has(o2))
                return i.get(o2);
              var u = e3.apply(this, n3);
              return r3.cache = i.set(o2, u) || i, u;
            };
            return r3.cache = new (o.Cache || n2)(), r3;
          }
          o.Cache = n2, e2.exports = o;
        }, 479: function(e2) {
          e2.exports = function() {
            return [];
          };
        }, 5062: function(e2) {
          e2.exports = function() {
            return false;
          };
        }, 9833: function(e2, t2, r2) {
          var n2 = r2(531);
          e2.exports = function(e3) {
            return null == e3 ? "" : n2(e3);
          };
        } }, t = {};
        function r(n2) {
          var o = t[n2];
          if (void 0 !== o)
            return o.exports;
          var i = t[n2] = { id: n2, loaded: false, exports: {} };
          return e[n2](i, i.exports, r), i.loaded = true, i.exports;
        }
        r.n = function(e2) {
          var t2 = e2 && e2.__esModule ? function() {
            return e2.default;
          } : function() {
            return e2;
          };
          return r.d(t2, { a: t2 }), t2;
        }, r.d = function(e2, t2) {
          for (var n2 in t2)
            r.o(t2, n2) && !r.o(e2, n2) && Object.defineProperty(e2, n2, { enumerable: true, get: t2[n2] });
        }, r.g = function() {
          if ("object" == typeof globalThis)
            return globalThis;
          try {
            return this || new Function("return this")();
          } catch (e2) {
            if ("object" == typeof window)
              return window;
          }
        }(), r.o = function(e2, t2) {
          return Object.prototype.hasOwnProperty.call(e2, t2);
        }, r.r = function(e2) {
          "undefined" != typeof Symbol && Symbol.toStringTag && Object.defineProperty(e2, Symbol.toStringTag, { value: "Module" }), Object.defineProperty(e2, "__esModule", { value: true });
        }, r.nmd = function(e2) {
          return e2.paths = [], e2.children || (e2.children = []), e2;
        };
        var n = {};
        return function() {
          "use strict";
          r.r(n), r.d(n, { Collection: function() {
            return d;
          }, FetchServer: function() {
            return N;
          }, Server: function() {
            return S;
          }, Single: function() {
            return b;
          }, default: function() {
            return $;
          } });
          var e2 = r(7361), t2 = r.n(e2), o = r(6410), i = r.n(o);
          function u(e3, t3) {
            if (!(e3 instanceof t3))
              throw new TypeError("Cannot call a class as a function");
          }
          function a(e3, t3) {
            for (var r2 = 0; r2 < t3.length; r2++) {
              var n2 = t3[r2];
              n2.enumerable = n2.enumerable || false, n2.configurable = true, "value" in n2 && (n2.writable = true), Object.defineProperty(e3, n2.key, n2);
            }
          }
          function c(e3, t3, r2) {
            return t3 in e3 ? Object.defineProperty(e3, t3, { value: r2, enumerable: true, configurable: true, writable: true }) : e3[t3] = r2, e3;
          }
          function s(e3, t3) {
            return function(e4) {
              if (Array.isArray(e4))
                return e4;
            }(e3) || function(e4, t4) {
              var r2 = null == e4 ? null : "undefined" != typeof Symbol && e4[Symbol.iterator] || e4["@@iterator"];
              if (null == r2)
                return;
              var n2, o2, i2 = [], u2 = true, a2 = false;
              try {
                for (r2 = r2.call(e4); !(u2 = (n2 = r2.next()).done) && (i2.push(n2.value), !t4 || i2.length !== t4); u2 = true)
                  ;
              } catch (e5) {
                a2 = true, o2 = e5;
              } finally {
                try {
                  u2 || null == r2.return || r2.return();
                } finally {
                  if (a2)
                    throw o2;
                }
              }
              return i2;
            }(e3, t3) || function(e4, t4) {
              if (!e4)
                return;
              if ("string" == typeof e4)
                return f(e4, t4);
              var r2 = Object.prototype.toString.call(e4).slice(8, -1);
              "Object" === r2 && e4.constructor && (r2 = e4.constructor.name);
              if ("Map" === r2 || "Set" === r2)
                return Array.from(e4);
              if ("Arguments" === r2 || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r2))
                return f(e4, t4);
            }(e3, t3) || function() {
              throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.");
            }();
          }
          function f(e3, t3) {
            (null == t3 || t3 > e3.length) && (t3 = e3.length);
            for (var r2 = 0, n2 = new Array(t3); r2 < t3; r2++)
              n2[r2] = e3[r2];
            return n2;
          }
          function l(e3) {
            return l = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(e4) {
              return typeof e4;
            } : function(e4) {
              return e4 && "function" == typeof Symbol && e4.constructor === Symbol && e4 !== Symbol.prototype ? "symbol" : typeof e4;
            }, l(e3);
          }
          var p = function(e3, r2) {
            if (-1 !== e3.indexOf("_q")) {
              var n2 = e3.replace(/(_q)$/, ""), o2 = new RegExp(r2, "i");
              return function(e4) {
                var r3;
                return null !== (null === (r3 = t2()(e4, n2)) || void 0 === r3 ? void 0 : r3.match(o2));
              };
            }
            if (-1 !== e3.indexOf("_lte")) {
              var u2 = e3.replace(/(_lte)$/, "");
              return function(e4) {
                return t2()(e4, u2) <= r2;
              };
            }
            if (-1 !== e3.indexOf("_gte")) {
              var a2 = e3.replace(/(_gte)$/, "");
              return function(e4) {
                return t2()(e4, a2) >= r2;
              };
            }
            if (-1 !== e3.indexOf("_lt")) {
              var c2 = e3.replace(/(_lt)$/, "");
              return function(e4) {
                return t2()(e4, c2) < r2;
              };
            }
            if (-1 !== e3.indexOf("_gt")) {
              var s2 = e3.replace(/(_gt)$/, "");
              return function(e4) {
                return t2()(e4, s2) > r2;
              };
            }
            if (-1 !== e3.indexOf("_neq_any")) {
              var f2 = e3.replace(/(_neq_any)$/, ""), p2 = Array.isArray(r2) ? r2 : [r2];
              return function(e4) {
                return p2.every(function(r3) {
                  return t2()(e4, f2) != r3;
                });
              };
            }
            if (-1 !== e3.indexOf("_neq")) {
              var y2 = e3.replace(/(_neq)$/, "");
              return function(e4) {
                return t2()(e4, y2) != r2;
              };
            }
            if (-1 !== e3.indexOf("_eq_any")) {
              var d2 = e3.replace(/(_eq_any)$/, ""), h2 = Array.isArray(r2) ? r2 : [r2];
              return function(e4) {
                return h2.some(function(r3) {
                  return t2()(e4, d2) == r3;
                });
              };
            }
            if (-1 !== e3.indexOf("_eq")) {
              var v2 = e3.replace(/(_eq)$/, "");
              return function(e4) {
                return t2()(e4, v2) == r2;
              };
            }
            if (-1 !== e3.indexOf("_inc_any")) {
              var b2 = e3.replace(/(_inc_any)$/, ""), g2 = Array.isArray(r2) ? r2 : [r2];
              return function(e4) {
                return g2.some(function(r3) {
                  return t2()(e4, b2).includes(r3);
                });
              };
            }
            if (-1 !== e3.indexOf("_inc")) {
              var m2 = e3.replace(/(_inc)$/, ""), j2 = Array.isArray(r2) ? r2 : [r2];
              return function(e4) {
                return j2.every(function(r3) {
                  return t2()(e4, m2).includes(r3);
                });
              };
            }
            if (-1 !== e3.indexOf("_ninc_any")) {
              var x2 = e3.replace(/(_ninc_any)$/, ""), _2 = Array.isArray(r2) ? r2 : [r2];
              return function(e4) {
                return _2.every(function(r3) {
                  return !t2()(e4, x2).includes(r3);
                });
              };
            }
            return Array.isArray(r2) ? function(n3) {
              return Array.isArray(t2()(n3, e3)) ? (o3 = function(r3) {
                return o4 = t2()(n3, e3), i2 = function(e4) {
                  return e4 == r3;
                }, o4.reduce(function(e4, t3) {
                  return e4 || i2(t3);
                }, false);
                var o4, i2;
              }, r2.reduce(function(e4, t3) {
                return e4 && o3(t3);
              }, true)) : r2.filter(function(r3) {
                return r3 == t2()(n3, e3);
              }).length > 0;
              var o3;
            } : "object" === l(r2) ? function(n3) {
              return i()(r2)(t2()(n3, e3));
            } : function(n3) {
              return Array.isArray(t2()(n3, e3)) && "string" == typeof r2 ? -1 !== t2()(n3, e3).indexOf(r2) : "boolean" == typeof t2()(n3, e3) && "string" == typeof r2 ? t2()(n3, e3) == ("true" === r2) : t2()(n3, e3) == r2;
            };
          };
          function y(e3, r2) {
            if ("function" == typeof r2)
              return e3.filter(r2);
            if (r2 instanceof Object) {
              var n2 = Object.keys(r2).map(function(e4) {
                if ("q" === e4) {
                  var n3 = new RegExp(r2.q, "i");
                  return function e5(t3) {
                    for (var r3 in t3) {
                      if ("object" === l(t3[r3]) && e5(t3[r3]))
                        return true;
                      if (t3[r3] && t3[r3].match && null !== t3[r3].match(n3))
                        return true;
                    }
                    return false;
                  };
                }
                var o2 = e4.split("."), i2 = r2[e4];
                return o2.length > 1 ? function(r3) {
                  var n4 = function(e5, r4) {
                    return e5.reduce(function(n5, o3, i3) {
                      if (null != n5)
                        return n5;
                      var u3 = e5.slice(0, i3 + 1).join("."), a3 = e5.slice(i3 + 1).join("."), c2 = t2()(r4, u3);
                      return Array.isArray(c2) && i3 < e5.length - 1 ? [u3, a3] : void 0;
                    }, void 0);
                  }(o2, r3);
                  if (n4) {
                    var u2 = s(n4, 2), a2 = u2[0], f2 = u2[1];
                    return y(t2()(r3, a2), c({}, f2, i2)).length > 0;
                  }
                  return p(e4, i2)(r3);
                } : p(e4, i2);
              });
              return e3.filter(function(e4) {
                return n2.reduce(function(t3, r3) {
                  return t3 && r3(e4);
                }, true);
              });
            }
            throw new Error("Unsupported filter type");
          }
          var d = function() {
            function e3() {
              var t4 = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : [], r3 = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : "id";
              if (u(this, e3), c(this, "sequence", 0), c(this, "items", []), c(this, "server", null), c(this, "name", null), c(this, "identifierName", "id"), !Array.isArray(t4))
                throw new Error("Can't initialize a Collection with anything else than an array of items");
              this.identifierName = r3, t4.map(this.addOne.bind(this));
            }
            var t3, r2, n2;
            return t3 = e3, (r2 = [{ key: "setServer", value: function(e4) {
              this.server = e4;
            } }, { key: "setName", value: function(e4) {
              this.name = e4;
            } }, { key: "_oneToManyEmbedder", value: function(e4) {
              var t4 = this;
              if (null == this.name)
                throw new Error("Can't embed references without a collection name");
              var r3 = this.name.slice(0, -1) + "_id";
              return function(n3) {
                if (null == t4.server)
                  throw new Error("Can't embed references without a server");
                var o2 = t4.server.collections[e4];
                if (!o2)
                  throw new Error("Can't embed a non-existing collection ".concat(e4));
                return Array.isArray(n3[e4]) ? n3[e4] = o2.getAll({ filter: function(t5) {
                  return -1 !== n3[e4].indexOf(t5[o2.identifierName]);
                } }) : n3[e4] = o2.getAll({ filter: function(e5) {
                  return e5[r3] == n3[t4.identifierName];
                } }), n3;
              };
            } }, { key: "_manyToOneEmbedder", value: function(e4) {
              var t4 = this, r3 = e4 + "s", n3 = e4 + "_id";
              return function(o2) {
                if (null == t4.server)
                  throw new Error("Can't embed references without a server");
                var i2 = t4.server.collections[r3];
                if (!i2)
                  throw new Error("Can't embed a non-existing collection ".concat(e4));
                try {
                  o2[e4] = i2.getOne(o2[n3]);
                } catch (e5) {
                }
                return o2;
              };
            } }, { key: "_itemEmbedder", value: function(e4) {
              var t4 = this, r3 = (Array.isArray(e4) ? e4 : [e4]).map(function(e5) {
                return e5.endsWith("s") ? t4._oneToManyEmbedder(e5) : t4._manyToOneEmbedder(e5);
              });
              return function(e5) {
                return r3.reduce(function(e6, t5) {
                  return t5(e6);
                }, e5);
              };
            } }, { key: "getCount", value: function(e4) {
              return this.getAll(e4).length;
            } }, { key: "getAll", value: function(e4) {
              var t4 = this.items.slice(0);
              return e4 && (e4.filter && (t4 = y(t4, e4.filter)), e4.sort && (t4 = function(e5, t5) {
                if ("function" == typeof t5)
                  return e5.sort(t5);
                if ("string" == typeof t5)
                  return e5.sort(function(e6, r4) {
                    return e6[t5] > r4[t5] ? 1 : e6[t5] < r4[t5] ? -1 : 0;
                  });
                if (Array.isArray(t5)) {
                  var r3 = t5[0], n3 = "asc" == t5[1].toLowerCase() ? 1 : -1;
                  return e5.sort(function(e6, t6) {
                    return e6[r3] > t6[r3] ? n3 : e6[r3] < t6[r3] ? -1 * n3 : 0;
                  });
                }
                throw new Error("Unsupported sort type");
              }(t4, e4.sort)), e4.range && (t4 = function(e5, t5) {
                if (Array.isArray(t5))
                  return e5.slice(t5[0], void 0 !== t5[1] ? t5[1] + 1 : void 0);
                throw new Error("Unsupported range type");
              }(t4, e4.range)), t4 = t4.map(function(e5) {
                return Object.assign({}, e5);
              }), e4.embed && this.server && (t4 = t4.map(this._itemEmbedder(e4.embed)))), t4;
            } }, { key: "getIndex", value: function(e4) {
              var t4 = this;
              return this.items.findIndex(function(r3) {
                return r3[t4.identifierName] == e4;
              });
            } }, { key: "getOne", value: function(e4, t4) {
              var r3 = this.getIndex(e4);
              if (-1 === r3)
                throw new Error("No item with identifier ".concat(e4));
              var n3 = this.items[r3];
              return n3 = Object.assign({}, n3), t4 && t4.embed && this.server && (n3 = this._itemEmbedder(t4.embed)(n3)), n3;
            } }, { key: "addOne", value: function(e4) {
              var t4 = e4[this.identifierName];
              if (void 0 !== t4) {
                if (-1 !== this.getIndex(t4))
                  throw new Error("An item with the identifier ".concat(t4, " already exists"));
                this.sequence = Math.max(this.sequence, t4) + 1;
              } else
                e4[this.identifierName] = this.sequence++;
              return this.items.push(e4), Object.assign({}, e4);
            } }, { key: "updateOne", value: function(e4, t4) {
              var r3 = this.getIndex(e4);
              if (-1 === r3)
                throw new Error("No item with identifier ".concat(e4));
              for (var n3 in t4)
                this.items[r3][n3] = t4[n3];
              return Object.assign({}, this.items[r3]);
            } }, { key: "removeOne", value: function(e4) {
              var t4 = this.getIndex(e4);
              if (-1 === t4)
                throw new Error("No item with identifier ".concat(e4));
              var r3 = this.items[t4];
              return this.items.splice(t4, 1), e4 == this.sequence - 1 && this.sequence--, r3;
            } }]) && a(t3.prototype, r2), n2 && a(t3, n2), Object.defineProperty(t3, "prototype", { writable: false }), e3;
          }();
          function h(e3, t3) {
            for (var r2 = 0; r2 < t3.length; r2++) {
              var n2 = t3[r2];
              n2.enumerable = n2.enumerable || false, n2.configurable = true, "value" in n2 && (n2.writable = true), Object.defineProperty(e3, n2.key, n2);
            }
          }
          function v(e3, t3, r2) {
            return t3 in e3 ? Object.defineProperty(e3, t3, { value: r2, enumerable: true, configurable: true, writable: true }) : e3[t3] = r2, e3;
          }
          var b = function() {
            function e3(t4) {
              if (function(e4, t5) {
                if (!(e4 instanceof t5))
                  throw new TypeError("Cannot call a class as a function");
              }(this, e3), v(this, "obj", null), v(this, "server", null), v(this, "name", null), !(t4 instanceof Object))
                throw new Error("Can't initialize a Single with anything except an object");
              this.obj = t4;
            }
            var t3, r2, n2;
            return t3 = e3, (r2 = [{ key: "setServer", value: function(e4) {
              this.server = e4;
            } }, { key: "setName", value: function(e4) {
              this.name = e4;
            } }, { key: "_oneToManyEmbedder", value: function(e4) {
              var t4 = this;
              return function(r3) {
                if (null == t4.server)
                  throw new Error("Can't embed references without a server");
                var n3 = t4.server.collections[e4];
                if (!n3)
                  throw new Error("Can't embed a non-existing collection ".concat(e4));
                return r3[e4] = n3.getAll({ filter: function(t5) {
                  return -1 !== r3[e4].indexOf(t5[n3.identifierName]);
                } }), r3;
              };
            } }, { key: "_manyToOneEmbedder", value: function(e4) {
              var t4 = this, r3 = e4 + "s", n3 = e4 + "_id";
              return function(o2) {
                if (null == t4.server)
                  throw new Error("Can't embed references without a server");
                var i2 = t4.server.collections[r3];
                if (!i2)
                  throw new Error("Can't embed a non-existing collection ".concat(e4));
                try {
                  o2[e4] = i2.getOne(o2[n3]);
                } catch (e5) {
                }
                return o2;
              };
            } }, { key: "_itemEmbedder", value: function(e4) {
              var t4 = this, r3 = (Array.isArray(e4) ? e4 : [e4]).map(function(e5) {
                return e5.endsWith("s") ? t4._oneToManyEmbedder(e5) : t4._manyToOneEmbedder(e5);
              });
              return function(e5) {
                return r3.reduce(function(e6, t5) {
                  return t5(e6);
                }, e5);
              };
            } }, { key: "getOnly", value: function(e4) {
              var t4 = this.obj;
              return e4 && e4.embed && this.server && (t4 = Object.assign({}, t4), t4 = this._itemEmbedder(e4.embed)(t4)), t4;
            } }, { key: "updateOnly", value: function(e4) {
              for (var t4 in e4)
                this.obj[t4] = e4[t4];
              return this.obj;
            } }]) && h(t3.prototype, r2), n2 && h(t3, n2), Object.defineProperty(t3, "prototype", { writable: false }), e3;
          }();
          function g(e3, t3) {
            return function(e4) {
              if (Array.isArray(e4))
                return e4;
            }(e3) || function(e4, t4) {
              var r2 = null == e4 ? null : "undefined" != typeof Symbol && e4[Symbol.iterator] || e4["@@iterator"];
              if (null == r2)
                return;
              var n2, o2, i2 = [], u2 = true, a2 = false;
              try {
                for (r2 = r2.call(e4); !(u2 = (n2 = r2.next()).done) && (i2.push(n2.value), !t4 || i2.length !== t4); u2 = true)
                  ;
              } catch (e5) {
                a2 = true, o2 = e5;
              } finally {
                try {
                  u2 || null == r2.return || r2.return();
                } finally {
                  if (a2)
                    throw o2;
                }
              }
              return i2;
            }(e3, t3) || function(e4, t4) {
              if (!e4)
                return;
              if ("string" == typeof e4)
                return m(e4, t4);
              var r2 = Object.prototype.toString.call(e4).slice(8, -1);
              "Object" === r2 && e4.constructor && (r2 = e4.constructor.name);
              if ("Map" === r2 || "Set" === r2)
                return Array.from(e4);
              if ("Arguments" === r2 || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r2))
                return m(e4, t4);
            }(e3, t3) || function() {
              throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.");
            }();
          }
          function m(e3, t3) {
            (null == t3 || t3 > e3.length) && (t3 = e3.length);
            for (var r2 = 0, n2 = new Array(t3); r2 < t3; r2++)
              n2[r2] = e3[r2];
            return n2;
          }
          function j(e3) {
            if (!e3)
              return {};
            var t3 = {};
            return e3.split("&").map(function(e4) {
              if (-1 === e4.indexOf("="))
                t3[e4] = true;
              else {
                var r2 = g(e4.split("="), 2), n2 = r2[0], o2 = r2[1];
                0 !== o2.indexOf("[") && 0 !== o2.indexOf("{") || (o2 = JSON.parse(o2)), t3[n2.trim()] = o2;
              }
            }), t3;
          }
          function x(e3, t3) {
            var r2 = "undefined" != typeof Symbol && e3[Symbol.iterator] || e3["@@iterator"];
            if (!r2) {
              if (Array.isArray(e3) || (r2 = function(e4, t4) {
                if (!e4)
                  return;
                if ("string" == typeof e4)
                  return _(e4, t4);
                var r3 = Object.prototype.toString.call(e4).slice(8, -1);
                "Object" === r3 && e4.constructor && (r3 = e4.constructor.name);
                if ("Map" === r3 || "Set" === r3)
                  return Array.from(e4);
                if ("Arguments" === r3 || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r3))
                  return _(e4, t4);
              }(e3)) || t3 && e3 && "number" == typeof e3.length) {
                r2 && (e3 = r2);
                var n2 = 0, o2 = function() {
                };
                return { s: o2, n: function() {
                  return n2 >= e3.length ? { done: true } : { done: false, value: e3[n2++] };
                }, e: function(e4) {
                  throw e4;
                }, f: o2 };
              }
              throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.");
            }
            var i2, u2 = true, a2 = false;
            return { s: function() {
              r2 = r2.call(e3);
            }, n: function() {
              var e4 = r2.next();
              return u2 = e4.done, e4;
            }, e: function(e4) {
              a2 = true, i2 = e4;
            }, f: function() {
              try {
                u2 || null == r2.return || r2.return();
              } finally {
                if (a2)
                  throw i2;
              }
            } };
          }
          function _(e3, t3) {
            (null == t3 || t3 > e3.length) && (t3 = e3.length);
            for (var r2 = 0, n2 = new Array(t3); r2 < t3; r2++)
              n2[r2] = e3[r2];
            return n2;
          }
          function O(e3, t3) {
            if (!(e3 instanceof t3))
              throw new TypeError("Cannot call a class as a function");
          }
          function w(e3, t3) {
            for (var r2 = 0; r2 < t3.length; r2++) {
              var n2 = t3[r2];
              n2.enumerable = n2.enumerable || false, n2.configurable = true, "value" in n2 && (n2.writable = true), Object.defineProperty(e3, n2.key, n2);
            }
          }
          function A(e3, t3, r2) {
            return t3 in e3 ? Object.defineProperty(e3, t3, { value: r2, enumerable: true, configurable: true, writable: true }) : e3[t3] = r2, e3;
          }
          var S = function() {
            function e3() {
              var t4 = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : "";
              O(this, e3), A(this, "baseUrl", null), A(this, "loggingEnabled", false), A(this, "defaultQuery", function() {
              }), A(this, "batchUrl", null), A(this, "collections", {}), A(this, "singles", {}), A(this, "requestInterceptors", []), A(this, "responseInterceptors", []), this.baseUrl = t4;
            }
            var t3, r2, n2;
            return t3 = e3, r2 = [{ key: "init", value: function(e4) {
              for (var t4 in e4)
                Array.isArray(e4[t4]) ? this.addCollection(t4, new d(e4[t4], "id")) : this.addSingle(t4, new b(e4[t4]));
            } }, { key: "toggleLogging", value: function() {
              this.loggingEnabled = !this.loggingEnabled;
            } }, { key: "setDefaultQuery", value: function(e4) {
              this.defaultQuery = e4;
            } }, { key: "setBatchUrl", value: function(e4) {
              this.batchUrl = e4;
            } }, { key: "setBatch", value: function(e4) {
              console.warn("Server.setBatch() is deprecated, use Server.setBatchUrl() instead"), this.batchUrl = e4;
            } }, { key: "addCollection", value: function(e4, t4) {
              this.collections[e4] = t4, t4.setServer(this), t4.setName(e4);
            } }, { key: "getCollection", value: function(e4) {
              return this.collections[e4];
            } }, { key: "getCollectionNames", value: function() {
              return Object.keys(this.collections);
            } }, { key: "addSingle", value: function(e4, t4) {
              this.singles[e4] = t4, t4.setServer(this), t4.setName(e4);
            } }, { key: "getSingle", value: function(e4) {
              return this.singles[e4];
            } }, { key: "getSingleNames", value: function() {
              return Object.keys(this.singles);
            } }, { key: "addRequestInterceptor", value: function(e4) {
              this.requestInterceptors.push(e4);
            } }, { key: "addResponseInterceptor", value: function(e4) {
              this.responseInterceptors.push(e4);
            } }, { key: "getCount", value: function(e4, t4) {
              return this.collections[e4].getCount(t4);
            } }, { key: "getAll", value: function(e4, t4) {
              return this.collections[e4].getAll(t4);
            } }, { key: "getOne", value: function(e4, t4, r3) {
              return this.collections[e4].getOne(t4, r3);
            } }, { key: "addOne", value: function(e4, t4) {
              return this.collections.hasOwnProperty(e4) || this.addCollection(e4, new d([], "id")), this.collections[e4].addOne(t4);
            } }, { key: "updateOne", value: function(e4, t4, r3) {
              return this.collections[e4].updateOne(t4, r3);
            } }, { key: "removeOne", value: function(e4, t4) {
              return this.collections[e4].removeOne(t4);
            } }, { key: "getOnly", value: function(e4, t4) {
              return this.singles[e4].getOnly();
            } }, { key: "updateOnly", value: function(e4, t4) {
              return this.singles[e4].updateOnly(t4);
            } }, { key: "decode", value: function(e4) {
              if (e4.queryString = decodeURIComponent(e4.url.slice(e4.url.indexOf("?") + 1)), e4.params = j(e4.queryString), e4.requestBody)
                try {
                  e4.json = JSON.parse(e4.requestBody);
                } catch (e5) {
                }
              return this.requestInterceptors.reduce(function(e5, t4) {
                return t4(e5);
              }, e4);
            } }, { key: "respond", value: function(e4, t4, r3) {
              var n3 = arguments.length > 3 && void 0 !== arguments[3] ? arguments[3] : 200;
              t4 || (t4 = {}), t4["Content-Type"] || (t4["Content-Type"] = "application/json");
              var o2 = { status: n3, headers: t4, body: e4 };
              return o2 = this.responseInterceptors.reduce(function(e5, t5) {
                return t5(e5, r3);
              }, o2), this.log(r3, o2), r3.respond(o2.status, o2.headers, JSON.stringify(o2.body));
            } }, { key: "log", value: function(e4, t4) {
              this.loggingEnabled && (console.group ? (console.groupCollapsed(e4.method, e4.url, "(FakeRest)"), console.group("request"), console.log(e4.method, e4.url), console.log("headers", e4.requestHeaders), console.log("body   ", e4.requestBody), console.groupEnd(), console.group("response", t4.status), console.log("headers", t4.headers), console.log("body   ", t4.body), console.groupEnd(), console.groupEnd()) : (console.log("FakeRest request ", e4.method, e4.url, "headers", e4.requestHeaders, "body", e4.requestBody), console.log("FakeRest response", t4.status, "headers", t4.headers, "body", t4.body)));
            } }, { key: "batch", value: function(e4) {
              var t4 = e4.json, r3 = this.handle.bind(this), n3 = Object.keys(t4).reduce(function(e5, n4) {
                var o2, i2 = { url: t4[n4], method: "GET", params: {}, respond: function(e6, t5, r4) {
                  o2 = { code: e6, headers: Object.keys(t5 || {}).map(function(e7) {
                    return { name: e7, value: t5[e7] };
                  }), body: r4 || {} };
                } };
                return r3(i2), e5[n4] = o2 || { code: 404, headers: [], body: {} }, e5;
              }, {});
              return this.respond(n3, {}, e4, 200);
            } }, { key: "handle", value: function(e4) {
              if (e4 = this.decode(e4), this.batchUrl && this.batchUrl === e4.url && "POST" === e4.method)
                return this.batch(e4);
              var t4, r3 = x(this.getSingleNames());
              try {
                for (r3.s(); !(t4 = r3.n()).done; ) {
                  var n3 = t4.value;
                  if (e4.url.match(new RegExp("^" + this.baseUrl + "\\/(" + n3 + ")(\\/?.*)?$"))) {
                    if ("GET" == e4.method)
                      try {
                        var o2 = this.getOnly(n3);
                        return this.respond(o2, null, e4);
                      } catch (t5) {
                        return e4.respond(404);
                      }
                    if ("PUT" == e4.method)
                      try {
                        var i2 = this.updateOnly(n3, e4.json);
                        return this.respond(i2, null, e4);
                      } catch (t5) {
                        return e4.respond(404);
                      }
                    if ("PATCH" == e4.method)
                      try {
                        var u2 = this.updateOnly(n3, e4.json);
                        return this.respond(u2, null, e4);
                      } catch (t5) {
                        return e4.respond(404);
                      }
                  }
                }
              } catch (e5) {
                r3.e(e5);
              } finally {
                r3.f();
              }
              var a2 = e4.url.match(new RegExp("^" + this.baseUrl + "\\/([^\\/?]+)(\\/(\\d+))?(\\?.*)?$"));
              if (a2) {
                var c2 = a2[1], s2 = Object.assign({}, this.defaultQuery(c2), e4.params);
                if (a2[2]) {
                  if (!this.getCollection(c2))
                    return;
                  var f2 = a2[3];
                  if ("GET" == e4.method)
                    try {
                      var l2 = this.getOne(c2, f2, s2);
                      return this.respond(l2, null, e4);
                    } catch (t5) {
                      return e4.respond(404);
                    }
                  if ("PUT" == e4.method)
                    try {
                      var p2 = this.updateOne(c2, f2, e4.json);
                      return this.respond(p2, null, e4);
                    } catch (t5) {
                      return e4.respond(404);
                    }
                  if ("PATCH" == e4.method)
                    try {
                      var y2 = this.updateOne(c2, f2, e4.json);
                      return this.respond(y2, null, e4);
                    } catch (t5) {
                      return e4.respond(404);
                    }
                  if ("DELETE" == e4.method)
                    try {
                      var d2 = this.removeOne(c2, f2);
                      return this.respond(d2, null, e4);
                    } catch (t5) {
                      return e4.respond(404);
                    }
                } else {
                  if ("GET" == e4.method) {
                    if (!this.getCollection(c2))
                      return;
                    var h2, v2, b2, g2 = this.getCount(c2, s2.filter ? { filter: s2.filter } : {});
                    if (g2 > 0) {
                      h2 = this.getAll(c2, s2);
                      var m2 = s2.range ? s2.range[0] : 0, j2 = s2.range ? Math.min(h2.length - 1 + m2, s2.range[1]) : h2.length - 1;
                      v2 = "items ".concat(m2, "-").concat(j2, "/").concat(g2), b2 = h2.length == g2 ? 200 : 206;
                    } else
                      h2 = [], v2 = "items */0", b2 = 200;
                    return this.respond(h2, { "Content-Range": v2 }, e4, b2);
                  }
                  if ("POST" == e4.method) {
                    var _2 = this.addOne(c2, e4.json), O2 = this.baseUrl + "/" + c2 + "/" + _2[this.getCollection(c2).identifierName];
                    return this.respond(_2, { Location: O2 }, e4, 201);
                  }
                }
              }
            } }, { key: "getHandler", value: function() {
              return this.handle.bind(this);
            } }], r2 && w(t3.prototype, r2), n2 && w(t3, n2), Object.defineProperty(t3, "prototype", { writable: false }), e3;
          }();
          function E(e3) {
            return E = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(e4) {
              return typeof e4;
            } : function(e4) {
              return e4 && "function" == typeof Symbol && e4.constructor === Symbol && e4 !== Symbol.prototype ? "symbol" : typeof e4;
            }, E(e3);
          }
          function k(e3, t3) {
            var r2 = "undefined" != typeof Symbol && e3[Symbol.iterator] || e3["@@iterator"];
            if (!r2) {
              if (Array.isArray(e3) || (r2 = function(e4, t4) {
                if (!e4)
                  return;
                if ("string" == typeof e4)
                  return C(e4, t4);
                var r3 = Object.prototype.toString.call(e4).slice(8, -1);
                "Object" === r3 && e4.constructor && (r3 = e4.constructor.name);
                if ("Map" === r3 || "Set" === r3)
                  return Array.from(e4);
                if ("Arguments" === r3 || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r3))
                  return C(e4, t4);
              }(e3)) || t3 && e3 && "number" == typeof e3.length) {
                r2 && (e3 = r2);
                var n2 = 0, o2 = function() {
                };
                return { s: o2, n: function() {
                  return n2 >= e3.length ? { done: true } : { done: false, value: e3[n2++] };
                }, e: function(e4) {
                  throw e4;
                }, f: o2 };
              }
              throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.");
            }
            var i2, u2 = true, a2 = false;
            return { s: function() {
              r2 = r2.call(e3);
            }, n: function() {
              var e4 = r2.next();
              return u2 = e4.done, e4;
            }, e: function(e4) {
              a2 = true, i2 = e4;
            }, f: function() {
              try {
                u2 || null == r2.return || r2.return();
              } finally {
                if (a2)
                  throw i2;
              }
            } };
          }
          function C(e3, t3) {
            (null == t3 || t3 > e3.length) && (t3 = e3.length);
            for (var r2 = 0, n2 = new Array(t3); r2 < t3; r2++)
              n2[r2] = e3[r2];
            return n2;
          }
          function T(e3, t3) {
            if (!(e3 instanceof t3))
              throw new TypeError("Cannot call a class as a function");
          }
          function P(e3, t3) {
            for (var r2 = 0; r2 < t3.length; r2++) {
              var n2 = t3[r2];
              n2.enumerable = n2.enumerable || false, n2.configurable = true, "value" in n2 && (n2.writable = true), Object.defineProperty(e3, n2.key, n2);
            }
          }
          function q(e3, t3) {
            return q = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(e4, t4) {
              return e4.__proto__ = t4, e4;
            }, q(e3, t3);
          }
          function I(e3) {
            var t3 = function() {
              if ("undefined" == typeof Reflect || !Reflect.construct)
                return false;
              if (Reflect.construct.sham)
                return false;
              if ("function" == typeof Proxy)
                return true;
              try {
                return Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
                })), true;
              } catch (e4) {
                return false;
              }
            }();
            return function() {
              var r2, n2 = R(e3);
              if (t3) {
                var o2 = R(this).constructor;
                r2 = Reflect.construct(n2, arguments, o2);
              } else
                r2 = n2.apply(this, arguments);
              return U(this, r2);
            };
          }
          function U(e3, t3) {
            if (t3 && ("object" === E(t3) || "function" == typeof t3))
              return t3;
            if (void 0 !== t3)
              throw new TypeError("Derived constructors may only return object or undefined");
            return function(e4) {
              if (void 0 === e4)
                throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
              return e4;
            }(e3);
          }
          function R(e3) {
            return R = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(e4) {
              return e4.__proto__ || Object.getPrototypeOf(e4);
            }, R(e3);
          }
          var N = function(e3) {
            !function(e4, t4) {
              if ("function" != typeof t4 && null !== t4)
                throw new TypeError("Super expression must either be null or a function");
              e4.prototype = Object.create(t4 && t4.prototype, { constructor: { value: e4, writable: true, configurable: true } }), Object.defineProperty(e4, "prototype", { writable: false }), t4 && q(e4, t4);
            }(i2, e3);
            var t3, r2, n2, o2 = I(i2);
            function i2() {
              return T(this, i2), o2.apply(this, arguments);
            }
            return t3 = i2, (r2 = [{ key: "decode", value: function(e4, t4) {
              var r3 = this, n3 = "string" == typeof e4 ? new Request(e4, t4) : e4;
              return n3.queryString = decodeURIComponent(n3.url.slice(n3.url.indexOf("?") + 1)), n3.params = j(n3.queryString), n3.text().then(function(e5) {
                n3.requestBody = e5;
                try {
                  n3.requestJson = JSON.parse(e5);
                } catch (e6) {
                }
              }).then(function() {
                return r3.requestInterceptors.reduce(function(e5, t5) {
                  return t5(e5);
                }, n3);
              });
            } }, { key: "respond", value: function(e4, t4) {
              return e4 = this.responseInterceptors.reduce(function(e5, r3) {
                return r3(e5, t4);
              }, e4), this.log(t4, e4), e4.headers = new Headers(e4.headers), e4;
            } }, { key: "log", value: function(e4, t4) {
              this.loggingEnabled && (console.group ? (console.groupCollapsed(e4.method, e4.url, "(FakeRest)"), console.group("request"), console.log(e4.method, e4.url), console.log("headers", e4.headers), console.log("body   ", e4.requestBody), console.groupEnd(), console.group("response", t4.status), console.log("headers", t4.headers), console.log("body   ", t4.body), console.groupEnd(), console.groupEnd()) : (console.log("FakeRest request ", e4.method, e4.url, "headers", e4.headers, "body", e4.requestBody), console.log("FakeRest response", t4.status, "headers", t4.headers, "body", t4.body)));
            } }, { key: "batch", value: function(e4) {
              throw new Error("not implemented");
            } }, { key: "handle", value: function(e4, t4) {
              var r3 = this;
              return this.decode(e4, t4).then(function(e5) {
                var t5 = { headers: { "Content-Type": "application/json" }, status: 200 };
                if (r3.batchUrl && r3.batchUrl === e5.url && "POST" === e5.method)
                  return r3.batch(e5);
                var n3, o3 = k(r3.getSingleNames());
                try {
                  for (o3.s(); !(n3 = o3.n()).done; ) {
                    var i3 = n3.value;
                    if (e5.url.match(new RegExp("^" + r3.baseUrl + "\\/(" + i3 + ")(\\/?.*)?$"))) {
                      if ("GET" == e5.method) {
                        try {
                          t5.body = r3.getOnly(i3);
                        } catch (e6) {
                          reponse.status = 404;
                        }
                        return r3.respond(t5, e5);
                      }
                      if ("PUT" == e5.method) {
                        try {
                          t5.body = r3.updateOnly(i3, e5.requestJson);
                        } catch (e6) {
                          reponse.status = 404;
                        }
                        return r3.respond(t5, e5);
                      }
                      if ("PATCH" == e5.method) {
                        try {
                          t5.body = r3.updateOnly(i3, e5.requestJson);
                        } catch (e6) {
                          reponse.status = 404;
                        }
                        return r3.respond(t5, e5);
                      }
                    }
                  }
                } catch (e6) {
                  o3.e(e6);
                } finally {
                  o3.f();
                }
                var u2, a2 = k(r3.getCollectionNames());
                try {
                  for (a2.s(); !(u2 = a2.n()).done; ) {
                    var c2 = u2.value, s2 = e5.url.match(new RegExp("^" + r3.baseUrl + "\\/(" + c2 + ")(\\/(\\d+))?(\\?.*)?$"));
                    if (s2) {
                      var f2 = Object.assign({}, r3.defaultQuery(c2), e5.params);
                      if (s2[2]) {
                        var l2 = s2[3];
                        if ("GET" == e5.method) {
                          try {
                            t5.body = r3.getOne(c2, l2, f2);
                          } catch (e6) {
                            t5.status = 404;
                          }
                          return r3.respond(t5, e5);
                        }
                        if ("PUT" == e5.method) {
                          try {
                            t5.body = r3.updateOne(c2, l2, e5.requestJson);
                          } catch (e6) {
                            t5.status = 404;
                          }
                          return r3.respond(t5, e5);
                        }
                        if ("PATCH" == e5.method) {
                          try {
                            t5.body = r3.updateOne(c2, l2, e5.requestJson);
                          } catch (e6) {
                            t5.status = 404;
                          }
                          return r3.respond(t5, e5);
                        }
                        if ("DELETE" == e5.method) {
                          try {
                            t5.body = r3.removeOne(c2, l2);
                          } catch (e6) {
                            t5.status = 404;
                          }
                          return r3.respond(t5, e5);
                        }
                      } else {
                        if ("GET" == e5.method) {
                          var p2 = r3.getCount(c2, f2.filter ? { filter: f2.filter } : {});
                          if (p2 > 0) {
                            var y2 = r3.getAll(c2, f2), d2 = f2.range ? f2.range[0] : 0, h2 = f2.range ? Math.min(y2.length - 1 + d2, f2.range[1]) : y2.length - 1;
                            t5.body = y2, t5.headers["Content-Range"] = "items ".concat(d2, "-").concat(h2, "/").concat(p2), t5.status = y2.length == p2 ? 200 : 206;
                          } else
                            t5.body = [], t5.headers["Content-Range"] = "items */0";
                          return r3.respond(t5, e5);
                        }
                        if ("POST" == e5.method) {
                          var v2 = r3.addOne(c2, e5.requestJson), b2 = r3.baseUrl + "/" + c2 + "/" + v2[r3.getCollection(c2).identifierName];
                          return t5.body = v2, t5.headers.Location = b2, t5.status = 201, r3.respond(t5, e5);
                        }
                      }
                    }
                  }
                } catch (e6) {
                  a2.e(e6);
                } finally {
                  a2.f();
                }
                return r3.respond(t5, e5);
              });
            } }]) && P(t3.prototype, r2), n2 && P(t3, n2), Object.defineProperty(t3, "prototype", { writable: false }), i2;
          }(S), $ = { Server: S, FetchServer: N, Collection: d, Single: b };
        }(), n;
      }();
    });
  }
});

// node_modules/ra-data-fakerest/dist/esm/index.js
var import_fakerest = __toESM(require_FakeRest_min());
var __extends = function() {
  var extendStatics = function(d, b) {
    extendStatics = Object.setPrototypeOf || { __proto__: [] } instanceof Array && function(d2, b2) {
      d2.__proto__ = b2;
    } || function(d2, b2) {
      for (var p in b2)
        if (Object.prototype.hasOwnProperty.call(b2, p))
          d2[p] = b2[p];
    };
    return extendStatics(d, b);
  };
  return function(d, b) {
    if (typeof b !== "function" && b !== null)
      throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
    extendStatics(d, b);
    function __() {
      this.constructor = d;
    }
    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
  };
}();
var __assign = function() {
  __assign = Object.assign || function(t) {
    for (var s, i = 1, n = arguments.length; i < n; i++) {
      s = arguments[i];
      for (var p in s)
        if (Object.prototype.hasOwnProperty.call(s, p))
          t[p] = s[p];
    }
    return t;
  };
  return __assign.apply(this, arguments);
};
function log(type, resource, params, response) {
  if (console.group) {
    console.groupCollapsed(type, resource, JSON.stringify(params));
    console.log(response);
    console.groupEnd();
  } else {
    console.log("FakeRest request ", type, resource, params);
    console.log("FakeRest response", response);
  }
}
var esm_default = function(data, loggingEnabled) {
  if (loggingEnabled === void 0) {
    loggingEnabled = false;
  }
  var restServer = new import_fakerest.default.Server();
  restServer.init(data);
  if (typeof window !== "undefined") {
    window.restServer = restServer;
  }
  function getResponse(type, resource, params) {
    var _a;
    switch (type) {
      case "getList": {
        var _b = params.pagination, page = _b.page, perPage = _b.perPage;
        var _c = params.sort, field = _c.field, order = _c.order;
        var query = {
          sort: [field, order],
          range: [(page - 1) * perPage, page * perPage - 1],
          filter: params.filter
        };
        return {
          data: restServer.getAll(resource, query),
          total: restServer.getCount(resource, {
            filter: params.filter
          })
        };
      }
      case "getOne":
        return {
          data: restServer.getOne(resource, params.id, __assign({}, params))
        };
      case "getMany":
        return {
          data: params.ids.map(function(id) {
            return restServer.getOne(resource, id);
          }, __assign({}, params))
        };
      case "getManyReference": {
        var _d = params.pagination, page = _d.page, perPage = _d.perPage;
        var _e = params.sort, field = _e.field, order = _e.order;
        var query = {
          sort: [field, order],
          range: [(page - 1) * perPage, page * perPage - 1],
          filter: __assign(__assign({}, params.filter), (_a = {}, _a[params.target] = params.id, _a))
        };
        return {
          data: restServer.getAll(resource, query),
          total: restServer.getCount(resource, {
            filter: query.filter
          })
        };
      }
      case "update":
        return {
          data: restServer.updateOne(resource, params.id, __assign({}, params.data))
        };
      case "updateMany":
        params.ids.forEach(function(id) {
          return restServer.updateOne(resource, id, __assign({}, params.data));
        });
        return { data: params.ids };
      case "create":
        return {
          data: restServer.addOne(resource, __assign({}, params.data))
        };
      case "delete":
        return { data: restServer.removeOne(resource, params.id) };
      case "deleteMany":
        params.ids.forEach(function(id) {
          return restServer.removeOne(resource, id);
        });
        return { data: params.ids };
      default:
        return false;
    }
  }
  var handle = function(type, resource, params) {
    var collection = restServer.getCollection(resource);
    if (!collection && type !== "create") {
      var error = new UndefinedResourceError('Undefined collection "'.concat(resource, '"'));
      error.code = 1;
      return Promise.reject(error);
    }
    var response;
    try {
      response = getResponse(type, resource, params);
    } catch (error2) {
      console.error(error2);
      return Promise.reject(error2);
    }
    if (loggingEnabled) {
      log(type, resource, params, response);
    }
    return Promise.resolve(response);
  };
  return {
    getList: function(resource, params) {
      return handle("getList", resource, params);
    },
    getOne: function(resource, params) {
      return handle("getOne", resource, params);
    },
    getMany: function(resource, params) {
      return handle("getMany", resource, params);
    },
    getManyReference: function(resource, params) {
      return handle("getManyReference", resource, params);
    },
    update: function(resource, params) {
      return handle("update", resource, params);
    },
    updateMany: function(resource, params) {
      return handle("updateMany", resource, params);
    },
    create: function(resource, params) {
      return handle("create", resource, params);
    },
    delete: function(resource, params) {
      return handle("delete", resource, params);
    },
    deleteMany: function(resource, params) {
      return handle("deleteMany", resource, params);
    }
  };
};
var UndefinedResourceError = (
  /** @class */
  function(_super) {
    __extends(UndefinedResourceError2, _super);
    function UndefinedResourceError2() {
      return _super !== null && _super.apply(this, arguments) || this;
    }
    return UndefinedResourceError2;
  }(Error)
);
export {
  esm_default as default
};
//# sourceMappingURL=ra-data-fakerest.js.map
