#! -*- coding:utf-8 -*-
'''
Created on 2017年11月10日

@author: zhang.meng
'''

class MyJs(object):
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
        index = -1;
        
        if (elm.hasAttribute('id')) {myId = elm.getAttribute('id');}
        if(elm.hasAttribute('class')){myClass= elm.localName.toLowerCase() + "[class='" + elm.getAttribute('class') + "']";}
        if(elm.localName.toLowerCase()=="input"){myName = elm.getAttribute('name');}
        
        
        
        for (var segs = []; elm && elm.nodeType == 1; elm = elm.parentNode) 
        { 
           index += 1;
            for (i = 1, sib = elm.previousSibling; sib; sib = sib.previousSibling) { 
                if (sib.localName == elm.localName)  i++; }; 
                segs.unshift(elm.localName.toLowerCase() + '[' + i + ']');
            };
        return segs.length ? '/' + segs.join('/') : null; 
    }; 
    
    function lookupElementByXPath(path) { 
        var evaluator = new XPathEvaluator(); 
        var result = evaluator.evaluate(path, document.documentElement, null,XPathResult.FIRST_ORDERED_NODE_TYPE, null); 
        return  result.singleNodeValue; 
    } 
    
    document.addEventListener("mouseover", DIOnMouseOver, true);
    document.addEventListener("mouseout", DIOnMouseOut, true);
    document.addEventListener("mousedown", DIOnMouseDown, true);
    
    //选定边框的样式
        function DIOnMouseOver(evt)
    {
        element = evt.target;   // not IE
    
        // set the border around the element
        element.style.borderWidth = '1px';
        element.style.borderStyle = 'outset';
       // element.style.boxShadow="2px 2px 2px #888888";
        element.style.borderColor = '#0099FF';
    }
    
    function DIOnMouseOut(evt)
    {
        evt.target.style.borderStyle = 'none';
        //evt.target.style.boxShadow='none';
    }
    
    
    function DIOnClick(evt)
    {
        var selection = evt.target.innerHTML;
        
        //alert('Element is: ' + evt.target.toString() + '\n\nSelection is:\n\n' + selection);
        return false;
    }
    
    function getTag(evt){
        myTag = evt.localName.toLowerCase();
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
        
        var frames= w.parent.document.getElementsByTagName('frame');
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
        ev.stopPropagation();
        ev.stopImmediatePropagation();
        
        if(ev.ctrlKey){
            currentFrame = getiframeId(ev.toElement);
            xpath = createXPathFromElement(ev.toElement);
            var myinput1 = document.createElement('input');
            myinput1.type = 'hidden';
            myinput1.id = 'elementXPath';
            myinput1.name = 'elementXPath';
            myinput1.value = xpath;
            
            var myinput2 = document.createElement('input');
            myinput2.type = 'hidden';
            myinput2.id = 'elementValue';
            myinput2.name = 'elementValue';
            myinput2.value = getValue(ev.target);
               
            var myinput3 = document.createElement('input');
            myinput3.type = 'hidden';
            myinput3.id = 'elementTag';
            myinput3.name = 'elementTag';
            myinput3.value = getTag(ev.toElement);
               
            var myinput4 = document.createElement('input');
            myinput4.type = 'hidden';
            myinput4.id = 'elementId';
            myinput4.name = 'elementId';
            myinput4.value = myId;
            
            var myinput5 = document.createElement('input');
            myinput5.type = 'hidden';
            myinput5.id = 'elementClass';
            myinput5.name = 'elementClass';
            myinput5.value = myClass;
            
            var myinput6 = document.createElement('input');
            myinput6.type = 'hidden';
            myinput6.id = 'elementInput';
            myinput6.name = 'elementInput';
            myinput6.value = myName;
            
            var myinput7 = document.createElement('input');
            myinput7.type = 'hidden';
            myinput7.id = 'elementIframe';
            myinput7.name = 'elementIframe';
            myinput7.value = currentFrame;
            
            var myinput8 = document.createElement('input');
            myinput8.type = 'hidden';
            myinput8.id = 'elementIframeType';
            myinput8.name = 'elementIframeType';
            myinput8.value = currentWindowType;
            
            var myinput9 = document.createElement('input');
            myinput9.type = 'hidden';
            myinput9.id = 'elementIframeIndex';
            myinput9.name = 'elementIframeIndex';
            myinput9.value = allIndexFrame;
            
            myId = "";
            myClass = "";
            myName = "";
            currentWindowType = [];
            allIndexFrame = [];
            
            myForm = window.top.document.getElementById("myform");
            
            myForm.innerHTML = "";
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
            if(ev.toElement.localName.toLowerCase()=="a"){
                href = ev.target.href;
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
            str = elem[elem.selectedIndex].text;
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
    
    """
    
    js_2 = """
    function readyDom() {
        var formElements=document.getElementsByTagName("form");
        for(var i=0;i<formElements.length;i++){formElements[i].setAttribute("target","");}
        
        var xpath = '';
        var o ;
        
        var iframeElement = document.createElement("frame");
        iframeElement.width = 0;
        iframeElement.height=0;
        iframeElement.setAttribute("name","abcdefg");
        
        var formElement = document.createElement("form");
        formElement.setAttribute("style","display: none;");
        formElement.setAttribute("name","myform");
        formElement.setAttribute("id","myform");
        formElement.setAttribute("action","http://127.0.0.1:9998/internet");
        formElement.setAttribute("method","post");
        formElement.setAttribute("target","abcdefg");
        
        document.getElementsByTagName('body')[0].appendChild(iframeElement);
        document.getElementsByTagName('body')[0].appendChild(formElement);
    }
    
    readyDom();
    
    """
