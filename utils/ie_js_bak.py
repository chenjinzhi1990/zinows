#! -*- coding:utf-8 -*-

class IeJs(object):
    js = r"""
    myId = "";
    myClass = "";
    myName = "";
    
    function getIframe(elm){
       t = window.frames;
       alert(t);
    }
    
    function createXPathFromElement(elm) { 
        var allNodes = document.getElementsByTagName('*');
        elementTagLower = elm.localName|| elm.nodeName;
        if (elm.hasAttribute('id')) {myId = elm.getAttribute('id');}
        if(elm.hasAttribute('class')){myClass= elementTagLower.toLowerCase() + "[class='" + elm.getAttribute('class') + "']";}
        if(elementTagLower.toLowerCase()=="input"){myName = elm.getAttribute('name');}
        
        for (var segs = []; elm && elm.nodeType == 1; elm = elm.parentNode) 
        { 
            for (i = 1, sib = elm.previousSibling; sib; sib = sib.previousSibling) { 
                if ((sib.localName||sib.nodeName) == (elm.localName||elm.nodeName))  i++; };
                segs.unshift((elm.localName||elm.nodeName).toLowerCase() + '[' + i + ']');
            };
        return segs.length ? '/' + segs.join('/') : null; 
    }; 
    
    function lookupElementByXPath(path) { 
        var evaluator = new XPathEvaluator(); 
        var result = evaluator.evaluate(path, document.documentElement, null,XPathResult.FIRST_ORDERED_NODE_TYPE, null); 
        return  result.singleNodeValue; 
    } 
    
    function readyDom() {
        var formElements=document.getElementsByTagName("form");
        for(var i=0;i<formElements.length;i++){formElements[i].setAttribute("target","");}
        
        var xpath = '';
        var o ;
        
        var iframeElement = document.createElement("frame");
        iframeElement.offsetWidth = 0;
        iframeElement.offsetHeight =0;
        iframeElement.setAttribute("name","abcdefg");
        
        var formElement = document.createElement("form");
        formElement.setAttribute("style","display: none;");
        formElement.setAttribute("name","myform");
        formElement.setAttribute("id","myform");
        formElement.setAttribute("action","http://localhost:9998/internet");
        formElement.setAttribute("method","post");
        formElement.setAttribute("target","abcdefg");
        
        document.getElementsByTagName('body')[0].appendChild(iframeElement);
        document.getElementsByTagName('body')[0].appendChild(formElement);
        
        setIntervalForMain();
    }
    
    function checkForm(){
        var checkedForm=document.getElementById("myform");
        if(checkedForm){
            console.log("have");
        }else{
            readyDom();
        }
    
    }
    checkForm();
    
    //选定边框的样式
        function DIOnMouseOver(evt)
    {
        element = evt.target || window.event.srcElement;   // not IE
    
        // set the border around the element
        element.style.borderWidth = '1px';
        element.style.borderStyle = 'solid';
       // element.style.boxShadow="2px 2px 2px #888888";
        element.style.borderColor = '#0099FF';
    }
    
    function DIOnMouseOut(evt)
    {
        element = evt.target || window.event.srcElement;
        
        element.style.borderWidth = '0.1px';
        element.style.borderStyle = 'solid';
        element.style.borderColor = '#F8F8F8';
    }
    
    
    function DIOnClick(evt)
    {
        var selection = evt.target.innerHTML;
        
        //alert('Element is: ' + evt.target.toString() + '\n\nSelection is:\n\n' + selection);
        return false;
    }
    
    function getTag(evt){
        myTag = (evt.localName|| evt.nodeName).toLowerCase();
        if (evt.hasAttribute('type')) {
            myType = evt.getAttribute('type');
            if(myType=='submit'){
            myTag='submit';
            }else if(myType=='button'){
            myTag='click';
            }else if(myType=='checkbox'){
            myTag='click';
            }
        }
        return myTag;
    }
    
    currentWindowType = [];
    allIndexFrame = [];
    
    function getiframeId(elem) {
    var thedoc = elem.parentNode;
    while (thedoc.nodeName != '#document') {
        thedoc = thedoc.parentNode;
    }
    
    currentIframe = getFrameForDocument(thedoc);
    
    currentWindow = [];
    
    if(currentIframe){
        allIndexFrame.push(myIframeIndex);
        
        myIframeId = currentIframe.getAttribute("id");
        myIframeName = currentIframe.getAttribute("name");
        
        
        if(myIframeId){
            currentWindow.push(myIframeId);
            currentWindowType.push("str");
        }else if(myIframeName){
            currentWindow.push(myIframeName);
            currentWindowType.push("str");
        }else{
            currentWindow.push(myIframeIndex);
            currentWindowType.push("int");
            }
    }
    
    while(currentIframe){
        var mywidow = currentIframe.contentWindow;
        currentIframe = getFrameForDocument(mywidow.parent.document);
        if(currentIframe){
        
        allIndexFrame.push(myIframeIndex);
        
        myIframeId = currentIframe.getAttribute("id");
        if(myIframeId){
            currentWindow.push(myIframeId);
            currentWindowType.push("str");
            continue;
        }
        myIframeName = currentIframe.getAttribute("name");
        if(myIframeName){
            currentWindow.push(myIframeName);
            currentWindowType.push("str");
            continue;
        }
        currentWindow.push(myIframeIndex);
        currentWindowType.push("int");
        }
    }
    currentWindowType.reverse()
    return currentWindow.reverse();
    }
    
    
    function getFramedWindow(f){
        if(f.parentNode == null)
            f = document.body.appendChild(f);
        var w = (f.contentWindow || f.contentDocument);
        if(w && w.nodeType && w.nodeType==9)
            w = (w.defaultView || w.parentWindow);
        return w;
    }
    
    myIframeIndex = undefined;
    function getFrameForDocument(document) {
        myIframeIndex = undefined;
        var w= document.defaultView || document.parentWindow;
        var frames= w.parent.document.getElementsByTagName('iframe');
        for (var i= frames.length; i-->0;) {
            var frame= frames[i];
            try {
                var d= frame.contentDocument || frame.contentWindow.document;
                if (d===document){
                    myIframeIndex = i;
                    return frame;
                }
                    
            } catch(e) {}
        }
    }
    
    function DIOnMouseDown(ev)
    {
        if(ev.stopPropagation)
            ev.stopPropagation();
        else
            ev.cancelBubble=true;

        if(ev.ctrlKey){
            ev = ev.target || window.event.srcElement; 
            
            currentFrame = getiframeId(ev);
            xpath = createXPathFromElement(ev);
            var myinput1 = document.createElement('input');
            myinput1.setAttribute("type","hidden");
            myinput1.setAttribute("id","elementXPath");
            myinput1.setAttribute("name","elementXPath");
            myinput1.setAttribute("value",xpath);
            
            var myinput2 = document.createElement('input');
            myinput2.setAttribute("type","hidden");
            myinput2.setAttribute("id","elementValue");
            myinput2.setAttribute("name","elementValue");
            myinput2.setAttribute("value",getValue(ev));
            
            var myinput3 = document.createElement('input');
            myinput3.setAttribute("type","hidden");
            myinput3.setAttribute("id","elementTag");
            myinput3.setAttribute("name","elementTag");
            myinput3.setAttribute("value",getTag(ev));
            
            var myinput4 = document.createElement('input');
            myinput4.setAttribute("type","hidden");
            myinput4.setAttribute("id","elementId");
            myinput4.setAttribute("name","elementId");
            myinput4.setAttribute("value",myId);
            
            var myinput5 = document.createElement('input');
            myinput5.setAttribute("type","hidden");
            myinput5.setAttribute("id","elementClass");
            myinput5.setAttribute("name","elementClass");
            myinput5.setAttribute("value",myClass);
            
            var myinput6 = document.createElement('input');
            myinput6.setAttribute("type","hidden");
            myinput6.setAttribute("id","elementInput");
            myinput6.setAttribute("name","elementInput");
            myinput6.setAttribute("value",myName);
            
            var myinput7 = document.createElement('input');
            myinput7.setAttribute("type","hidden");
            myinput7.setAttribute("id","elementIframe");
            myinput7.setAttribute("name","elementIframe");
            myinput7.setAttribute("value",currentFrame);
            
            var myinput8 = document.createElement('input');
            myinput8.setAttribute("type","hidden");
            myinput8.setAttribute("id","elementIframeType");
            myinput8.setAttribute("name","elementIframeType");
            myinput8.setAttribute("value",currentWindowType);
            
            var myinput9 = document.createElement('input');
            myinput9.setAttribute("type","hidden");
            myinput9.setAttribute("id","elementIframeIndex");
            myinput9.setAttribute("name","elementIframeIndex");
            myinput9.setAttribute("value",allIndexFrame);
               
               myId = "";
               myClass = "";
               myName = "";
               currentWindowType = [];
               allIndexFrame = [];
               myForm = window.top.document.getElementById("myform");
               myForm.innerHTML = '';
               myForm.appendChild(myinput1);
               myForm.appendChild(myinput2);
               myForm.appendChild(myinput3);
               myForm.appendChild(myinput4);
               myForm.appendChild(myinput5);
               myForm.appendChild(myinput6);
               myForm.appendChild(myinput7);
               myForm.appendChild(myinput8);
               myForm.appendChild(myinput9);
               myForm.submit();
               return false;
        }else if(ev.altKey){
            ev = ev.target || window.event.srcElement; 
            if((ev.localName|| ev.nodeName).toLowerCase()=="a"){
                href = ev.href;
                location.href = href;
            }
            return false;
        }
    return true;
    }
    
    
    //获取选定元素的值
    function getValue(elem) {
        var str = '';
        switch (elem.tagName) {
        case 'A':
            str = (elem.innerText.length != 0) ? elem.innerText : elem.className;
            break;
        case 'INPUT':
            str = elem.value;
            break;
        case 'OPTION':
            str = elem.value;
            break;
        case 'SELECT':
            str = elem[elem.selectedIndex].value;
            break;
        case 'TEXTAREA':
            str = elem.value;
            break;
        default:
            str = elem.innerText;
        }
        if(str){
            return str.trim();
        }
        return "nothing";
        
    }
    
    function setIntervalForMain(){
        setInterval(function(){
            var nodes = document.all;  
            for(var i=0;i<nodes.length;i++){  
                var o = nodes[i];  
                if (o.hasAttribute('uniquedFlag')){
                    console.log('weiyi');
                }else{
                    o.setAttribute("uniquedFlag","weiyi");
                    if (o.addEventListener) {
                            o.addEventListener("mouseover", DIOnMouseOver, true);
                            o.addEventListener("mouseout", DIOnMouseOut, true);
                            o.addEventListener("mousedown", DIOnMouseDown, true);
                        }else {
                            o.attachEvent("onmouseover", DIOnMouseOver, true);
                            o.attachEvent("onmouseout", DIOnMouseOut, true);
                            o.attachEvent("onmousedown", DIOnMouseDown, true);
                        }
                }
            }
            forEveryIframe(document);
        
        }, 5000);
    
    }
    
    function forEveryIframe(loopDoc){
        var iframes = loopDoc.getElementsByTagName('iframe');
        for(var i=0; i<iframes.length; i++){
            curIfr = iframes[i];
            
            nextDoc = curIfr.contentWindow.document
            var nodess = nextDoc.all;
            for(var j=0;j<nodess.length;j++){  
                var o = nodess[j];
                if (o.hasAttribute('uniquedFlag')){
                    console.log('weiyi');
                }else{
                    o.setAttribute("uniquedFlag","weiyi");
                    if (o.addEventListener) {
                            o.addEventListener("mouseover", DIOnMouseOver, true);
                            o.addEventListener("mouseout", DIOnMouseOut, true);
                            o.addEventListener("mousedown", DIOnMouseDown, true);
                        }else {
                            o.attachEvent("onmouseover", DIOnMouseOver, true);
                            o.attachEvent("onmouseout", DIOnMouseOut, true);
                            o.attachEvent("onmousedown", DIOnMouseDown, true);
                        }
                }
            }
            forEveryIframe(nextDoc);
        }
    }
    
    String.prototype.trim = function() {
        return this.replace(/^\s+|\s+$/g,"");
    }
    """
    
