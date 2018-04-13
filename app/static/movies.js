// Movie api

var apiMovieWanna = function(form, callback){
     var path = '/api/movie/wanna'
     ajax('POST', path, form, callback)
}

var apiMovieSeen = function(form, callback){
     var path = '/api/movie/seen'
     ajax('POST', path, form, callback)
}


var bindEventWeiboAdd = function() {
    var b = e('#id-button-add')
    // 注意, 第二个参数可以直接给出定义函数
    b.addEventListener('click', function(){
        var input = e('#id-input-weibo')
        var title = input.value
        log('click add', title)
        var form = {
            content: title,
        }
        apiWeiboAdd(form, function(r) {
            // 收到返回的数据, 插入到页面中
            var weibo = JSON.parse(r)
            insertWeibo(weibo)
        })
    })
}


var bindEventMovieWanna = function() {
    var movieList = e('#id-movie-list')
    // 事件响应函数会传入一个参数 就是事件本身
    movieList.addEventListener('click', function(event) {
    log(event)
    // 我们可以通过 event.target 来得到被点击的对象
    var self = event.target
    log('被点击的元素', self)
    // 通过比较被点击元素的 class
    // 来判断元素是否是我们想要的
    // classList 属性保存了元素所有的 class
    log(self.classList)
    if (self.classList.contains('movie-wanna')) {
        log('点到了想看按钮')
        movie_id = self.parentElement.dataset['id']
        var form = {
            id: movie_id
        }
        apiMovieWanna(form, function(response){
            var r = JSON.parse(response)
            if (r.message=='已想看'){
                self.innerText = '已想看'
            }

        })
    } else {
        log('点到了 无关内容')
    }
})}

var bindEventMovieSeen = function() {
    var movieList = e('#id-movie-list')
    // 事件响应函数会传入一个参数 就是事件本身
    movieList.addEventListener('click', function(event) {
    log(event)
    // 我们可以通过 event.target 来得到被点击的对象
    var self = event.target
    log('被点击的元素', self)
    // 通过比较被点击元素的 class
    // 来判断元素是否是我们想要的
    // classList 属性保存了元素所有的 class
    log(self.classList)
    if (self.classList.contains('movie-seen')) {
        log('点到了想看按钮')
        movie_id = self.parentElement.dataset['id']
        log('movie_id是', movie_id)
        var form = {
            id: movie_id
        }
        apiMovieSeen(form, function(response){
            var r = JSON.parse(response)
            if (r.message=='已看过'){
                self.innerText = '已看过'
            }

        })
    } else {
        log('点到了 无关内容')
    }
})}



var bindEvents = function() {
    bindEventMovieSeen()
    bindEventMovieWanna()
}

var __main = function() {
    bindEvents()
}

__main()
