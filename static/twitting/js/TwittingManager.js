class TwittingManager {
    constructor(comments, can_write, user_id) {
        this.user_id = user_id;
        this.comments = comments;

        Array.from(this.comments).forEach(comment => {
            this.create_a_comment_box(comment);
            Array.from(comment.replys).forEach(reply => {
                this.create_a_comment_box(reply);
            })
        });

        this.init_new_posting();
    }


    create_a_comment_box(comment) {
        let comment_box = new CommentManager(comment);
        comment_box.add_listener(this.edit_post.bind(this), 'submit');
        comment_box.add_listener(this.like_post.bind(this), 'like');
        comment_box.add_listener(this.dislike_post.bind(this), 'dislike');
        comment_box.add_listener(this.delete_post.bind(this), 'delete');
        comment_box.add_listener(this.reply_post.bind(this), 'reply');
        comment_box.add_listener(this.edit_post.bind(this), 'heavy edit');
    }


    init_new_posting() {
        let button = document.getElementById('new-post');
        button.onclick = create_a_function_to_call_on_editor_result(this.new_post);
    }

    new_post(post_content) {
        alert('new post: ' + post_content);
    }


    edit_post(content, post_id) {
        alert('edit post\n' + post_id + '\n' + content);
    }

    delete_post(content, post_id) {

        alert(post_id + ' was deleted');
    }

    like_post(post_id) {
        alert(post_id + ' was liked');
    }

    dislike_post(post_id) {
        alert(post_id + ' was disliked');
    }

    reply_post(post_id, post_content) {
        alert(post_id + ' was replyed by text :' + post_content);
    }
}


class CommentManager {
    constructor(comment) {
        this.comment = comment;
        this.comment_box = document.getElementById(comment.id);

        this.comment_head = document.createElement('div');
        this.comment_content = document.createElement('div');
        this.comment_content.className = 'comment-content';
        this.comment_head.className = 'comment-head';
        this.comment_box.appendChild(this.comment_head);
        this.comment_box.appendChild(this.comment_content);

        this.init_head();

        this.init_content();

        this.init_editing_rules();

        this.init_editing_off_on();
    }

    init_head() {
        this.author_name = document.createElement('h6');
        this.author_name.className = "comment-name by-author";
        this.author_name.innerText = this.comment.author.name;
        this.comment_head.appendChild(this.author_name);
        this.time = document.createElement('span');
        this.time.innerText = this.comment.time;
        this.comment_head.appendChild(this.time);
        this.icons_container = document.createElement('div');
        this.icons_container.className = 'icons-pack';
        this.comment_head.appendChild(this.icons_container);
        this.iconsManager = new IconsManager(this.icons_container, this.comment.editable, this.comment.like_pack);
    }

    init_content() {
        this.comment_content.innerText = this.comment.content;
        this.comment_content.id = this.comment.id + '-content';
        this.editor = new FroalaEditor('#' + this.comment_content.id, {
            attribution: false,
            charCounterCount: false,
            toolbarInline: true,
        }, function () {
            this.edit.off();
            this.toolbar.hide();
        });
        window.e = this.editor;
    }

    init_editing_rules() {
        this.iconsManager.add_listener(function () {
            this.last_content = clone(this.editor.html.get());
        }.bind(this), 'edit');

        this.iconsManager.add_listener(function () {
            this.editor.html.set(this.last_content);
        }.bind(this), 'cancel');
        this.iconsManager.set_validation_of_submit(function () {
            return this.editor.html.get() !== '';
        }.bind(this), 'submit')
    }


    init_editing_off_on() {
        this.iconsManager.add_listener(function () {
            this.editor.edit.on();
            this.editor.toolbar.show();
        }.bind(this), 'edit');
        this.iconsManager.add_listener(function () {
            this.editor.edit.off();
            this.editor.toolbar.hide();
        }.bind(this), 'submit');
        this.iconsManager.add_listener(function () {
            this.editor.edit.off();
            this.editor.toolbar.hide();
        }.bind(this), 'cancel')
    }


    add_listener(f, func_name) {

        if (func_name === 'reply') {
            let get_text_from_editor = function (editor_text) {
                f(this.comment.id, editor_text);
            }.bind(this);
            let func = create_a_function_to_call_on_editor_result(get_text_from_editor);
            this.iconsManager.add_listener(func, 'reply');
            return;
        }

        if (func_name === 'heavy edit') {
            let get_text_from_editor = function (editor_text) {
                f(this.comment.id, editor_text);
            }.bind(this);
            let func = create_a_function_to_call_on_editor_result(get_text_from_editor, this.editor);
            this.iconsManager.add_listener(func, 'heavy edit');
            return;
        }

        if (func_name === 'like') {
            this.iconsManager.likeManager.add_listener_on_like(function () {
                f(this.comment.id);
            }.bind(this));
            return;
        }
        if (func_name === 'dislike') {
            this.iconsManager.likeManager.add_listener_on_dislike(function () {
                f(this.comment.id);
            }.bind(this));
            return;
        }

        this.iconsManager.add_listener(function () {
            f(this.editor.html.get(), this.comment.id);
        }.bind(this), func_name)
    }


}


class IconsManager {
    constructor(container, editable, like_pack) {
        this.in_edit_mode = false;
        this.container = container;

        this.like_container = document.createElement('div');
        this.like_container.className = 'like-pack';
        this.container.appendChild(this.like_container);
        this.likeManager = new LikeManager(this.like_container, like_pack);

        if (editable) {
            this.init_delete();
            this.init_edit();
            this.init_cancel();
            this.init_submit();
            this.init_reply();
            this.init_heavy_edit();
            this.container.appendChild(this.reply);
            this.container.appendChild(this.heavy_edit);
            this.container.appendChild(this.inline_edit);
            this.container.appendChild(this.delete);

        }

        this.funcs_on_edit = [];
        this.funcs_on_submit = [];
        this.funcs_on_cancel = [];
        this.funcs_on_delete = [];
        this.funcs_on_reply = [];
        this.funcs_on_heavy_edit = [];
        this.validation_of_submit = undefined;

        this.add_listener(this.edit_mode.bind(this), 'edit');
        this.add_listener(this.normal_mode.bind(this), 'cancel');
        this.add_listener(this.normal_mode.bind(this), 'submit');

    }

    init_heavy_edit() {
        this.heavy_edit = document.createElement('i');
        this.heavy_edit.className = 'pen square icon';
        this.heavy_edit.title = 'heavy edit';
        this.heavy_edit.onclick = this.heavy_edit_click.bind(this);
    }

    heavy_edit_click() {
        Array.from(this.funcs_on_heavy_edit).forEach(func => {
            func();
        })
    }

    init_edit() {
        this.inline_edit = document.createElement('i');
        this.inline_edit.className = 'edit icon mini-icon';
        this.inline_edit.title = 'inline edit';
        this.container.appendChild(this.inline_edit);
        this.inline_edit.onclick = this.edit_click.bind(this);
    }

    edit_click() {
        Array.from(this.funcs_on_edit).forEach(func => {
            func();
        })
    }

    init_delete() {
        this.delete = document.createElement('i');
        this.delete.title = 'delete';
        this.delete.className = 'trash alternate icon mini-icon';
        this.delete.onclick = this.delete_click.bind(this);
    }

    delete_click() {
        Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
        }).then((result) => {
            if (result.value) {
                Swal.fire(
                    'Deleted!',
                    'Your post has been deleted.',
                    'success'
                );
                Array.from(this.funcs_on_delete).forEach(func => {
                    func();
                });
            }
        });

    }

    init_cancel() {
        this.cancel = document.createElement('i');
        this.cancel.title = 'cancel';
        this.cancel.className = 'close red icon mini-icon';
        this.cancel.onclick = this.cancel_click.bind(this);
    }

    cancel_click() {
        Array.from(this.funcs_on_cancel).forEach(func => {
            func();
        })
    }

    init_reply() {
        this.reply = document.createElement('i');
        this.reply.className = 'reply icon';
        this.reply.title = 'reply';
        this.reply.onclick = this.reply_click.bind(this);
    }

    reply_click() {
        Array.from(this.funcs_on_reply).forEach(func => {
            func();
        })
    }

    init_submit() {
        this.submit = document.createElement('i');
        this.submit.title = 'submit';
        this.submit.className = 'check icon green mini-icon';
        this.submit.onclick = this.submit_click.bind(this);
    }

    submit_click() {
        if (this.validation_of_submit !== undefined) {
            let validation = this.validation_of_submit();
            if (validation === false) {
                this.cancel_click();
                Swal.fire({
                    icon: 'error',
                    title: 'Empty text ...!',
                });
                return;
            }
        }
        Array.from(this.funcs_on_submit).forEach(func => {
            func();
        })
    }

    normal_mode() {
        this.container.removeChild(this.submit);
        this.container.removeChild(this.cancel);
        this.container.appendChild(this.inline_edit);
        this.container.appendChild(this.delete);
        this.in_edit_mode = false;
    }

    edit_mode() {
        this.container.removeChild(this.inline_edit);
        this.container.removeChild(this.delete);
        this.container.appendChild(this.submit);
        this.container.appendChild(this.cancel);
        this.in_edit_mode = true;
    }

    add_listener(f, func_name) {
        let list;
        switch (func_name) {
            case 'delete':
                list = this.funcs_on_delete;
                break;
            case 'submit':
                list = this.funcs_on_submit;
                break;
            case 'edit':
                list = this.funcs_on_edit;
                break;
            case 'cancel':
                list = this.funcs_on_cancel;
                break;
            case 'reply':
                list = this.funcs_on_reply;
                break;
            case 'heavy edit':
                list = this.funcs_on_heavy_edit;
                break;
        }
        list.push(f);
    }

    set_validation_of_submit(f) {
        this.validation_of_submit = f;
    }
}


class LikeManager {
    constructor(container, like_pack) {
        this.like_pack = like_pack;
        this.container = container;
        this.init_icons();
        this.init_funcs();
    }

    init_icons() {

        this.like = document.createElement('i');
        this.like.className = 'thumbs up green icon';
        this.like.title = 'like';
        this.dislike = document.createElement('i');
        this.dislike.className = 'thumbs down red icon';
        this.dislike.title = 'dislike';
        this.like_counter = document.createElement('h4');
        this.like_counter.className = 'like-counter';
        this.like_counter.style.color = this.like_pack.like_numbers >= 0 ? 'green' : 'red';
        this.like_counter.innerText = this.like_pack.like_numbers;
        this.container.appendChild(this.like);
        this.container.appendChild(this.like_counter);
        this.container.appendChild(this.dislike);

    }


    update(like_pack) {
        this.like_counter.innerText = like_pack.like_counter;
    }


    init_funcs() {
        this.funcs_on_like = [];
        this.funcs_on_dislike = [];

        this.like.onclick = this.like_click.bind(this);
        this.dislike.onclick = this.dislike_click.bind(this);
    }


    like_click() {
        Array.from(this.funcs_on_like).forEach(func => {
            func();
        })
    }


    dislike_click() {
        Array.from(this.funcs_on_dislike).forEach(func => {
            func();
        })
    }

    add_listener_on_like(f) {
        this.funcs_on_like.push(f);
    }

    add_listener_on_dislike(f) {
        this.funcs_on_dislike.push(f);
    }
}


function clone(obj) {
    if (null == obj || "object" != typeof obj) return obj;
    var copy = obj.constructor();
    for (var attr in obj) {
        if (obj.hasOwnProperty(attr)) copy[attr] = obj[attr];
    }
    return copy;
}


function create_a_function_to_call_on_editor_result(func, inline_editor = undefined) {
    //this method get a function like func and return a function like f such that when you call f then
    // a text editor run and when text editor closed and was accept we call func by parameter of editor inner text
    return function () {
        (async () => {
            const {value: formValues} = await Swal.fire({
                width: '60%',
                confirmButtonText: 'send',
                showCancelButton: true,
                html: '<div id = "swal-editor" ></div>',
                onOpen: function () {
                    window.reply_post_editor = new FroalaEditor('#swal-editor', {
                        attribution: false,
                        charCounterCount: false,
                    }, function () {
                        if (inline_editor !== undefined) {
                            window.reply_post_editor.html.set(inline_editor.html.get());
                        }
                    });
                },
                focusConfirm: false,
                preConfirm: () => {

                }
            });
            if (formValues) {
                inline_editor.html.set(window.reply_post_editor.html.get());
                func(JSON.stringify(formValues));
            }
        })();
    };
}
