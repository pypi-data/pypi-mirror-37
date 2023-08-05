$(document).ready(function () {
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFToken';

    var new_feed = new Vue({
        el: '#new-feed',
        data: {
            content: '',
            success_message: '',
            error_message: '',
            selected_files: null,
        },

        methods: {
            on_upload_image_change: function (e) {
                if (e.target.files.length > 9) {
                    alert('最多只能传9张图片');
                    return;
                }

                this.selected_files = e.target.files;
                if (this.content.length === 0) {
                    this.content = '分享图片';
                }
            },

            post_new_feed: function (e) {
                e.target.disabled = true;
                var url = e.target.getAttribute("data-confirm");

                if (new_feed.content === '') {
                    alert('内容不能为空');
                } else {
                    var form_data = new FormData();
                    form_data.append('content', new_feed.content);
                    if (new_feed.selected_files) {
                        for (var i = 0; i < new_feed.selected_files.length; i++) {
                            var file = new_feed.selected_files[i];
                            form_data.append('files', file, file.name);
                        }
                    }

                    axios.post(url, form_data).then(function (resp) {
                        var data = resp.data;

                        if (data['rc'] === 0) {
                            new_feed.success_message = data['message'];

                            new_feed.content = '';
                            new_feed.selected_files = null;
                            setTimeout(function () {
                                new_feed.success_message = '';
                            }, 2000);

                            var new_feeds = JSON.parse(data['new_feeds']);
                            feeds.feeds = new_feeds.concat(feeds.feeds);
                        } else {
                            alert(data['message']);
                        }

                    });

                }
                e.target.disabled = false;
            }
        }
    });

    var feeds = new Vue({
        el: '#feeds',
        data: {
            feeds: [],
            page: 1,
            type: 0,   // 0 所有，1 单个用户, 2 同班同学（假的）
            user_id: 0,
            request_user_id: 0,
            can_manage: false // 当前用户是否可以管理日志
        },

        methods: {
            load_all_page: function (e) {
                e.preventDefault();
                feeds.user_id = 0;
                feeds.type = 0;
                feeds.page = 1;
                feeds.feeds = [];
                load_page_data();
            },

            load_classmates_page: function (user_id) {
                feeds.user_id = user_id;
                feeds.type = 2;
                feeds.page = 1;
                feeds.feeds = [];
                load_page_data();
            },

            load_my_page: function (user_id) {
                feeds.user_id = user_id;
                feeds.type = 1;
                feeds.page = 1;
                feeds.feeds = [];
                load_page_data();
            },

            remove_feed: function (feed_id) {
                for (var i=0; i<this.feeds.length; i++) {
                    var feed = this.feeds[i];
                    if (feed.id === feed_id) {
                        this.feeds.splice(i, 1);
                    }
                }
            }
        }
    });

    var loader = new Vue({
        el: '#feeds-loader',
        data: {
            status: 0
        },

        methods: {
            load_more_page: function (e) {
                e.preventDefault();

                feeds.page++;
                loader.status = 1;
                load_page_data();
            }
        }
    });

    Vue.component('image-list', {
        template: '#image-list',
        props: ['name'],
    });

    Vue.component('feed', {
        template: '#feed-template',
        props: ['id', 'publisher_data', 'content', 'emojis', 'comments', 'created_at', 'input_show',
            'link_name', 'link_link', 'images'],
        data: function () {
            return {
                data_id: this.id,
                data_publisher: this.publisher_data,
                data_content: this.content,
                data_emojis: this.emojis,
                data_comments: this.comments,
                data_created_at: this.created_at,
                data_input_show: this.input_show,
                data_link_name: this.link_name,
                data_link_link: this.link_link,
                new_comment: '',
                data_images: this.images,
                is_truncate: true,
                image_showbox_url: null,
                image_download_link: null,
            };
        },

        computed: {
            // 当前登录用户，是否给该条feed点过赞了？
            is_request_user_emoji: function () {
                var rc = false;

                if (typeof(this.data_emojis) === "undefined") {
                    return rc;
                }

                this.data_emojis.forEach(function (i) {
                    if (i.user_id === feeds.request_user_id) {
                        rc = true;
                    }
                });

                return rc;
            },

            // 该条feed 是否有人点赞了？
            has_emojis: function () {
                if (typeof(this.data_emojis) === "undefined") {
                    return false;
                } else {
                    return this.data_emojis.length > 0;
                }
            },

            // 是否有评论了
            has_comments: function () {
                if (typeof(this.data_comments) === "undefined") {
                    return false;
                } else {
                    return this.data_comments.length > 0;
                }
            },

            // 是否有链接名称
            has_link_name: function () {
                if (typeof(this.data_link_name) === "undefined") {
                    return false;
                } else {
                    return this.data_link_name != null;
                }
            },

            // 是否有链接内容
            has_link_link: function () {
                if (typeof(this.data_link_link) === "undefined") {
                    return false;
                } else {
                    return this.data_link_link != null;
                }
            },

            // 是否有传图片
            images_count: function () {
                if (typeof(this.data_images) === "undefined") {
                    return 0;
                } else {
                    if (this.data_images === null) {
                        return 0;
                    } else {
                        return this.data_images.length;
                    }
                }
            },
        },

        methods: {
            load_user_page: function (user_id, e) {
                e.preventDefault();
                feeds.user_id = user_id;
                feeds.type = 1;
                feeds.page = 1;
                feeds.feeds = [];
                load_page_data();
            },

            show_image: function(image) {
                this.image_showbox_url = image.medium_url;
                this.image_download_link = image.image;
            },

            fold_image: function() {
                this.image_showbox_url = null;
                this.image_download_link = null;
            },

            // 显示被截短的日志全文
            fold_content: function () {
                this.is_truncate = false;
            },

            // 收起日志全文
            unfold_content: function() {
                this.is_truncate = true;
            },

            // 点赞
            post_emoji: function (feed_id) {
                var this_feed = this;
                $.post('/feed/feeds/' + String(feed_id) + '/emoji')
                    .done(function (data) {
                        this_feed.data_emojis = this_feed.data_emojis.concat(JSON.parse(data['new_emoji']));
                    })
            },

            // 显示feed的评论输入框
            show_comment_input: function () {
                if (this.data_input_show) {
                    this.data_input_show = false;
                } else {
                    this.data_input_show = true;
                }
            },

            // 发表对feed的评论
            post_comment: function (feed_id, comment) {
                var this_feed = this;
                var post_data = {
                    comment: comment
                };
                $.post('/feed/feeds/' + String(feed_id) + '/comment', post_data)
                    .done(function (data) {
                        this_feed.data_comments = this_feed.data_comments.concat(JSON.parse(data['new_comments']));
                        this_feed.new_comment = '';
                        this_feed.data_input_show = false;
                    })
            },

            // 删除feed
            delete_feed: function (feed_id) {
                if (confirm('确定删除?')) {
                    var this_feed = this;
                    var url = "/feed/feeds/" + String(feed_id) + "/delete";
                    axios.post(url).then(function (resp) {
                        var data = resp['data'];
                        if (data['rc'] === 0) {
                            alert(data['message']);
                            feeds.remove_feed(feed_id);
                        }
                    });
                }

            },

            // 是否可以删除
            can_delete_feed: function (publisher_data) {
                if (feeds.can_manage) {
                    return true;
                } else {
                    return feeds.request_user_id === publisher_data.id;
                }
            },

            // 删除feed的评论
            delete_comment: function (comment_id) {
                if (confirm('确定删除评论？')) {
                    var _this = this;
                    var url = "/feed/feed_comment/" + String(comment_id) + '/delete';
                    axios.post(url).then(function (resp) {
                        var data = resp['data'];
                        if (data['rc'] === 0) {
                            alert(data['message']);
                            _this.remove_comment(comment_id);
                        }
                    });
                }
            },

            // 从this.comments里面移除comment_id对应的comment
            remove_comment: function(comment_id) {
                var comments = this.data_comments;
                for (var i=0; i<comments.length; i++) {
                    var comment = comments[i];
                    if (comment.id === comment_id) {
                        comments.splice(i, 1);
                    }
                }
            },

            // 是否可以删除评论
            can_delete_comment: function (publisher_data) {
                if (feeds.can_manage) {
                    return true;
                } else {
                    return feeds.request_user_id === publisher_data.id;
                }
            }
        },

        watch: {
            emojis(val) {
                this.data_emojis = val;
            },

            data_emojis(val) {
                this.$emit('update:emojis', val);
            },

            input_show(val) {
                this.data_input_show = val;
            },

            data_input_show(val) {
                this.$emit('update:input_show', val);
            },

            comments(val) {
                this.data_comments = val;
            },

            data_comments(val) {
                this.$emit('update:comments', val);
            },

            images(val) {
                this.data_images = val;
            },

            data_images(val) {
                this.$emit('update:images', val);
            }
        }
    });

    Vue.component('emoji-button', {
        template: '#emoji-button',
        props: ['feel']
    });

    Vue.component('emoji-did', {
        template: '#emoji-did'
    });

    Vue.component('comment-button', {
        template: '#comment-button',
        props: ['show_input']
    });

    moment.locale('zh-cn');
    Vue.filter('formatDate', function (value) {
        if (value) {
            return moment(String(value)).fromNow();
        }
    });

    Vue.filter('truncate', function (text, length, clamp) {
      text = text || '';
      clamp = clamp || '...';
      length = length || 140;

      if (text.length <= length) return text;

      var tcText = text.slice(0, length - clamp.length);
      var last = tcText.length - 1;


      while (last > 0 && tcText[last] !== ' ' && tcText[last] !== clamp[0]) last -= 1;

      // Fix for case when text dont have any `space`
      last = last || length - clamp.length;

      tcText =  tcText.slice(0, last);

      return tcText + clamp;
    });


    // 拉取指定页面的feeds
    var load_page_data = function () {
        var options = {
            page: feeds.page,
            type: feeds.type,
            user_id: feeds.user_id
        };

        $.get('/feed/feeds', options)
            .done(function (data) {
                var new_feeds = JSON.parse(data['feeds']);
                feeds.request_user_id = data['request_user_id'];
                feeds.can_manage = data['can_manage'];
                if (new_feeds.length === 0) {
                    feeds.page = data['page'];
                    loader.status = 3;
                } else {
                    feeds.feeds = feeds.feeds.concat(new_feeds);
                    feeds.page = data['page'];
                    loader.status = 0;
                }

                // console.log('第' + feeds.page + '页拉取完毕');
            })
            .fail(function () {
                loader.status = 2;
            })
    };
    load_page_data();

    // 下拉翻页的处理
    window.onscroll = function (e) {
        var bottomOfWindow = (window.scrollY  || window.pageYOffset || document.documentElement.scrollTop)
            + window.innerHeight >= document.documentElement.offsetHeight;

        if (bottomOfWindow) {
            loader.load_more_page(e);
        }
    }
});