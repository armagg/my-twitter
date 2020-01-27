class Comment {
    constructor(comment) {
        // let container = document.getElementById(comment.id);
        alert("");
        let editor = new FroalaEditor('#' + comment, {
            attribution: false,
            charCounterCount: false,
            toolbarInline: true,
        });
    }
}