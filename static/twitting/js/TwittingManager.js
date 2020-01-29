class TwittingManager {
    constructor(comments) {
        this.comments = comments;

        Array.from(this.comments).forEach(comment => {
            new CommentManager(comment);
            Array.from(comment.replys).forEach(reply => {
                new CommentManager(reply);
            })
        })

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
        this.author_name.innerText = '{{ reply.author.name }}';
        this.comment_head.appendChild(this.author_name);
        this.time = document.createElement('span');
        this.time.innerText = '{{ reply.time }}';
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
        },function () {
            this.edit.off();
        });
    }

    init_editing_rules() {
        this.iconsManager.add_listener(function () {
            this.last_content = clone(this.comment_content.innerHTML);
        }.bind(this), 'edit');

        this.iconsManager.add_listener(function () {
            this.comment_content.innerHTML = this.last_content;
        }.bind(this), 'cancel');
        this.iconsManager.set_validation_of_submit(function () {
            return this.editor.html.get() !== '';
        }.bind(this), 'submit')
    }


    init_editing_off_on() {
        this.iconsManager.add_listener(function () {
            console.log(this.editor);
            this.editor.edit.on();
        }.bind(this), 'edit');
        this.iconsManager.add_listener(function () {
            this.editor.edit.off();
        }.bind(this), 'submit');
        this.iconsManager.add_listener(function () {
            this.editor.edit.off();
        }.bind(this), 'cancel')
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
            this.init_edit();
            this.init_delete();
            this.init_cancel();
            this.init_submit();
            this.container.appendChild(this.delete);
            this.container.appendChild(this.edit);
        }

        this.funcs_on_edit = [];
        this.funcs_on_submit = [];
        this.funcs_on_cancel = [];
        this.funcs_on_delete = [];
        this.validation_of_submit = undefined;

        this.add_listener(this.edit_mode.bind(this), 'edit');
        this.add_listener(this.normal_mode.bind(this), 'cancel');
        this.add_listener(this.normal_mode.bind(this), 'submit');

    }

    init_edit() {
        this.edit = document.createElement('i');
        this.edit.className = 'edit icon mini-icon';
        this.edit.title = 'edit';
        this.container.appendChild(this.edit);
        this.edit.onclick = this.edit_click.bind(this);
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
        Array.from(this.funcs_on_delete).forEach(func => {
            func();
        })
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

    init_submit() {
        this.submit = document.createElement('i');
        this.submit.title = 'submit';
        this.submit.className = 'check icon green mini-icon';
        this.submit.onclick = this.submit_click.bind(this);
    }

    submit_click() {
        if (this.validation_of_submit !== undefined){
            if (this.validation_of_submit() === false){
                this.cancel_click();
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
        this.container.appendChild(this.edit);
        this.container.appendChild(this.delete);
        this.in_edit_mode = false;
    }

    edit_mode() {
        this.container.removeChild(this.edit);
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
        }
        list.push(f);
    }

    set_validation_of_submit(f){
        this.validation_of_submit = f;
    }
}


class LikeManager {
    constructor(container, like_pack) {

        this.like = document.createElement('i');
        this.like.className = 'thumbs up green icon';
        this.like.title = 'like';
        this.dislike = document.createElement('i');
        this.dislike.className = 'thumbs down red icon';
        this.dislike.title = 'dislike';
        this.like_counter = document.createElement('h4');
        this.like_counter.className = 'like-counter';
        this.like_counter.style.color = like_pack.like_numbers >= 0 ? 'green' : 'red';
        this.like_counter.innerText = like_pack.like_numbers;
        container.appendChild(this.like);
        container.appendChild(this.like_counter);
        container.appendChild(this.dislike);

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
