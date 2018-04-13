// Movie api

var apiMovieRemove = function(form, callback){
     var path = '/api/movie/remove'
     ajax('POST', path, form, callback)
}

var apiMovieSwiftSeen = function(form, callback){
     var path = '/api/movie/swift/wanna'
     ajax('POST', path, form, callback)
}

var apiMovieSwiftWanna = function(form, callback){
     var path = '/api/movie/swift/seen'
     ajax('POST', path, form, callback)
}

var bindEventMovieSwiftWanna = function() {
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
        apiMovieSwiftSeen(form, function(response){
            var r = JSON.parse(response)
            if (r.message=='已转换'){
                self.innerText = '已转换'
                self.style.backgroundColor = '#5bc0de'
            }
            self.innerText = '看过'
        })
    } else {
        log('点到了 无关内容')
    }
})}

var bindEventMovieSwiftSeen = function() {
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
        log('点到了看过按钮')
        movie_id = self.parentElement.dataset['id']
        var form = {
            id: movie_id
        }
        apiMovieSwiftSeen(form, function(response){
            var r = JSON.parse(response)
            if (r.message=='已转换'){
                self.innerText = '已转换'
            }
            self.innerText = '想看'
            self.style.backgroundColor = '#5cb85c'
        })
    } else {
        log('点到了 无关内容')
    }
})}

var bindEventMovieRemove = function() {
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
    if (self.classList.contains('movie-remove')) {
        log('点到了移除按钮')
        movie_id = self.parentElement.dataset['id']
        var form = {
            id: movie_id
        }
        apiMovieRemove(form, function(response){
            var r = JSON.parse(response)
            if (r.message=='已移除'){
                self.innerText = '已移除'
            }
            self.closest('.post').remove()
        })
    } else {
        log('点到了 无关内容')
    }
})}




var bindEvents = function() {
    bindEventMovieRemove()
    bindEventMovieSwiftWanna()
    bindEventMovieSwiftSeen()

}

var __main = function() {
    bindEvents()
}

__main()
