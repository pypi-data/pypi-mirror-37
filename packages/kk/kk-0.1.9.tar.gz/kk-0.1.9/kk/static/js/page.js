String.prototype.format = function () {
  var args = arguments;
  return this.replace(/{(\d+)}/g, function (match, number) {
    return typeof args[number] != 'undefined' ? args[number] : match;
  });
};

function getCookie(name) {
  var reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
  var arr = document.cookie.match(reg);
  return arr ? unescape(arr[2]) : null;
}

function setCookie(name, value, expires_days = 365) {
  var domain = location.host.split(":")[0];
  if (expires_days) {
    var exp = new Date();
    exp.setTime(exp.getTime() + expires_days * 86400000 + 8 * 3600000)
    document.cookie = name + '=' + value + ';path=/;domain=' + domain + ';expires=' + exp.toUTCString()

  } else {
    document.cookie = name + "=" + value + ";path=/;domain=" + domain + ";"
  }
}

function removeCookie(name) {
  setCookie(name, "", -1);
}

function parseUrl(url) {
  if (typeof url == 'undefined') {
    url = location.href;
  }
  var segment = url.match(/^(\w+\:\/\/)?([\w\d]+(?:\.[\w]+)*)?(?:\:(\d+))?(\/[^?#]*)?(?:\?([^#]*))?(?:#(.*))?$/);
  if (!segment[3]) {
    segment[3] = '80';
  }
  var param = {};
  if (segment[5]) {
    var pse = segment[5].match(/([^=&]+)=([^&]+)/g);
    if (pse) {
      for (var i = 0; i < pse.length; i++) {
        param[pse[i].split('=')[0]] = pse[i].split('=')[1];
      }
    }
  }
  return {
    url: segment[0],
    sechme: segment[1],
    host: segment[2],
    port: segment[3],
    path: segment[4],
    queryString: segment[5],
    fregment: segment[6],
    param: param
  };
};


$(function () {
  var clipboard = new ClipboardJS('.btn-copy', {
    target: function (trigger) {
      return $(trigger).parents('tr').find('input')[0]
    }
  })
  clipboard.on('success', function (e) {
    layer.msg('已复制到剪贴板', { time: 2000 })
    e.clearSelection()
  })

  clipboard.on('error', function (e) {
    layer.msg('复制出错，请手动复制', { time: 2000 })
  })
})
