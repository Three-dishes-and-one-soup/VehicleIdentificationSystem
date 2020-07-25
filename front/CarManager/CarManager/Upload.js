// author: 张嘉程
// createtime: 2020/7/12
// updatetime: 2020/7/25

var ep = new Vue({
    el: '#app',
    data: {
        imgUrl: "Pictures/Car/Mercedes.jpg"
    },
    methods: {
        showTheImg: function() {
            return { visible: false }
        },
        setUrl: function() {
            console.log("123");
        }
    }
});

document.getElementById('uploadImg').onchange = function(){
    //获取到文件
    f = this.files[0];
    console.log(this.files[0]);
    console.log(f);
    // console.dir(this);

    //限制上传的代码格式与大小
    var fileSize = this.files[0].size;
    var size = fileSize / 1024;

    if(size>2000){
        alert("附件不能大于2M");
        return
    }

    //限制上传的文件格式
    var name = this.files[0].name;
    var fileName = name.substring(name.lastIndexOf(".")+1).toLowerCase();
    if(fileName !="jpg" && fileName !="jpeg" && fileName !="pdf"
        && fileName !="png" && fileName !="dwg" && fileName !="gif" ){
        alert("请选择图片格式文件上传(jpg,png,gif,dwg,pdf,gif等)！");
        this.files[0].name = "";
        return
    }

    // 将文件生成一个url路径字符串
    var url = URL.createObjectURL(this.files[0]);

    // 将图片展示在div的盒子里面
    // document.querySelector('.imgShow').style.background = "url("+ url + ") no-repeat center/cover";

    //也可以将图片显示在img单标签里面
    document.querySelector('#backImg').src = url;
};

function uploadImage() {
    console.log("测试上传：");
    console.log(f);

    //1. 获取到上传的文件
    // var self = this;
    // console.log(form1.element.value);
    // let file = e.target.files[0];
    let file = f;

    //2. 创建form对象,将文件内容添加到form对象中
    let param = new FormData();  // 创建form对象
    param.append('file', file, file.name);  // 通过append向form对象添加数据
    param.append('functionType', 1);

    console.log("展示param：");
    console.log(param.get('file')); // FormData私有类对象，访问不到，可以通过get判断值是否传进去
    console.log(param.get('functionType'));

    // 设置请求头
    let config = {
        headers: {'Content-Type': 'multipart/form-data'}
    };

    // 添加请求头,发送请求头
    const url = "http://127.0.0.1:8000/api/license/result/";
    axios.post(url, param, config).then(response => {

        //打印请求成功后返回的值
        console.log(response.data);
    });
}