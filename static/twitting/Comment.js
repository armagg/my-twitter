class Comment2 {

    constructor(comment) {
        this.comment = comment;
        // // let container = document.getElementById(comment.id);
        // alert("");
        let editor = new FroalaEditor('#' + comment.id, {
            attribution: false,
            charCounterCount: false,
            toolbarInline: true,
        });
        alert('');
        this.create();

    }

    create = function (comment_box) {
        let comment_head = document.createElement('div');
        let comment_content = document.createElement('div');
        comment_content.className = 'comment_content';
        comment_head.className = 'comment_head';
        comment_box.appendChild(comment_head);
        comment_box.appendChild(comment_content);
        let author_name = document.createElement('h6');
        author_name.className = "comment-name by-author";
        author_name.innerText = this.comment.author_name;
        comment_head.appendChild(author_name);
        let time = document.createElement('span');
        time.innerText = this.comment.time;
        comment_head.appendChild(time);
        let icons_pack = document.createElement('div');
        icons_pack.className = 'icons-pack';
        comment_head.appendChild(icons_pack);
        comment_content.innerText = this.comment.content;
    }

}


// <div class="comment-head">
//                             <h6 class="comment-name by-author"><a
//                                     href="http://creaticode.com/blog">{{ comment.author.name }}</a>
//                             </h6>
//                             <div class="state">
//                                 {{ comment.author.state }}
//                             </div>
//                             <span>{{ comment.time }}</span>
//                             <div class="icons-pack" ></div>
//
//                             <i class="thumbs down red icon" title="like"></i>
//                             <i class="thumbs up green icon" title="dislike"></i>
//
//                             <i class="edit icon" title="edit"></i>
//                             <i class="trash alternate icon" title="delete"></i>
//                             <i class="check green icon" title="submit"></i>
//                             <i class="close red icon" title="cancel"></i>
//
//                             <i class="fa fa-reply"></i>
//                             <i class="fa fa-heart"></i>
//                         </div>
//                         <div class="comment-content" id="{{ comment.id }}">
//                             {{ comment.content }}
//                         </div>