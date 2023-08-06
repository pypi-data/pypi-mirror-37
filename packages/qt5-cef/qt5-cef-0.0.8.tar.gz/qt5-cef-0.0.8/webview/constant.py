default_window_width = -1
default_window_height = -1
default_window_title = 'FC-POS'
default_nest_window_margin = 0
min_window_width = 800
min_window_height = 800 * 0.618
language_locale = {
    '25': {
        'name': 'Chinese',
        'locale': 'zh_CN'
    },
    '59': {
        'name': 'Japanese',
        'locale': 'ja'
    }
}

burgeon_cef_sdk_js = r"""
(function () {
    if (window.CEF_HAS_INITIALIZED) {
        return
    }
    const encryptionKey = 'BURGEON-FRONT-END';
    const moduleName = 'windowInstance';
    const sdkModuleName = '__cef__';
    const pythonCallBack = 'python_cef';
    const cef = {
        payload: {},
        hooks: {}
    };
    const python_cef = {};
    const customEventMap = {
        windowCloseEvent: {
            name: 'windowCloseEvent',
            event: new CustomEvent('windowCloseEvent', {detail: {windowId: window.windowId}}),
            hooks: 0
        },
        windowBroadcastEvent: {
            name: 'windowBroadcastEvent',
            event: null,
            hooks: 0,
        }
    };
    python_cef.console = (msg, type) => {
        switch (type) {
            case 'error':
                console.error(msg);
                break;
            case 'warn':
                console.warn(msg);
                break;
            default:
                console.log(msg);
                break;
        }
    };
    python_cef.updateCustomizePayload = (params) => {
        Object.keys(params).forEach(key => {
            cef.payload[key] = params[key]
        })
    };
    python_cef.updateCefConfig = (key, value) => {
        if (window[sdkModuleName] === undefined) {
            window[sdkModuleName] = {}
        }
        window[sdkModuleName][key] = value;
    };
    python_cef.dispatchCustomEvent = (eventName, eventData) => {
        switch (eventName) {
            case customEventMap.windowCloseEvent.name:
                if (!window[moduleName] || typeof window[sdkModuleName]['close'] !== 'function') {
                    return;
                }
                if (customEventMap[eventName].hooks === 0) {
                    window[sdkModuleName].close();
                } else {
                    window.dispatchEvent(customEventMap[eventName].event)
                }
                break;
            case customEventMap.windowBroadcastEvent.name:
                const event = new CustomEvent(eventName, {detail: {eventData}});
                window.dispatchEvent(event);
                break;
            default:
                break;
        }

    };
    cef.VK_CODE = {
        'Backspace': 0x08,
        'Tab': 0x09,
        'Clear': 0x0C,
        'Enter': 0x0D,
        'Shift': 0x10,
        'Ctrl': 0x11,
        'Alt': 0x12,
        'Pause': 0x13,
        'CapsLock': 0x14,
        'Esc': 0x1B,
        'SpaceBar': 0x20,
        'PageUp': 0x21,
        'PageDown': 0x22,
        'End': 0x23,
        'Home': 0x24,
        'LeftArrow': 0x25,
        'UpArrow': 0x26,
        'RightArrow': 0x27,
        'DownArrow': 0x28,
        'Select': 0x29,
        'Print': 0x2A,
        'Execute': 0x2B,
        'PrintScreen': 0x2C,
        'Ins': 0x2D,
        'Del': 0x2E,
        'Help': 0x2F,
        '0': 0x30,
        '1': 0x31,
        '2': 0x32,
        '3': 0x33,
        '4': 0x34,
        '5': 0x35,
        '6': 0x36,
        '7': 0x37,
        '8': 0x38,
        '9': 0x39,
        'A': 0x41,
        'B': 0x42,
        'C': 0x43,
        'D': 0x44,
        'E': 0x45,
        'F': 0x46,
        'G': 0x47,
        'H': 0x48,
        'I': 0x49,
        'J': 0x4A,
        'K': 0x4B,
        'L': 0x4C,
        'M': 0x4D,
        'N': 0x4E,
        'O': 0x4F,
        'P': 0x50,
        'Q': 0x51,
        'R': 0x52,
        'S': 0x53,
        'T': 0x54,
        'U': 0x55,
        'V': 0x56,
        'W': 0x57,
        'X': 0x58,
        'Y': 0x59,
        'Z': 0x5A,
        'NumPad0': 0x60,
        'NumPad1': 0x61,
        'NumPad2': 0x62,
        'NumPad3': 0x63,
        'NumPad4': 0x64,
        'NumPad5': 0x65,
        'NumPad6': 0x66,
        'NumPad7': 0x67,
        'NumPad8': 0x68,
        'NumPad9': 0x69,
        'MultiplyKey': 0x6A,
        'AddKey': 0x6B,
        'SeparatorKey': 0x6C,
        'SubtractKey': 0x6D,
        'DecimalKey': 0x6E,
        'DivideKey': 0x6F,
        'F1': 0x70,
        'F2': 0x71,
        'F3': 0x72,
        'F4': 0x73,
        'F5': 0x74,
        'F6': 0x75,
        'F7': 0x76,
        'F8': 0x77,
        'F9': 0x78,
        'F10': 0x79,
        'F11': 0x7A,
        'F12': 0x7B,
        'F13': 0x7C,
        'F14': 0x7D,
        'F15': 0x7E,
        'F16': 0x7F,
        'F17': 0x80,
        'F18': 0x81,
        'F19': 0x82,
        'F20': 0x83,
        'F21': 0x84,
        'F22': 0x85,
        'F23': 0x86,
        'F24': 0x87,
        'NumLock': 0x90,
        'ScrollLock': 0x91,
        'LeftShift': 0xA0,
        'RightShift ': 0xA1,
        'LeftControl': 0xA2,
        'RightControl': 0xA3,
        'LeftMenu': 0xA4,
        'RightMenu': 0xA5,
        'BrowserBack': 0xA6,
        'BrowserForward': 0xA7,
        'BrowserRefresh': 0xA8,
        'BrowserStop': 0xA9,
        'BrowserSearch': 0xAA,
        'BrowserFavorites': 0xAB,
        'BrowserStartAndHome': 0xAC,
        'VolumeMute': 0xAD,
        'VolumeDown': 0xAE,
        'VolumeUp': 0xAF,
        'NextTrack': 0xB0,
        'PreviousTrack': 0xB1,
        'StopMedia': 0xB2,
        'Play/PauseMedia': 0xB3,
        'StartMail': 0xB4,
        'SelectMedia': 0xB5,
        'StartApplication1': 0xB6,
        'StartApplication2': 0xB7,
        'AttnKey': 0xF6,
        'CrselKey': 0xF7,
        'ExselKey': 0xF8,
        'PlayKey': 0xFA,
        'ZoomKey': 0xFB,
        'ClearKey': 0xFE,
    };
    cef.addEventListener = (eventName, eventHook) => {
        if (customEventMap[eventName] === undefined) {
            console.error(`window.${sdkModuleName}.addEventListener(eventName, eventHook) : eventName 必须是 ${Object.keys(customEventMap)} 中的一个`)
            return;
        }
        if (typeof eventHook !== 'function') {
            console.error(`window.${sdkModuleName}.addEventListener(eventName, eventHook): eventHook 必须是一个函数`);
            return;
        }
        customEventMap[eventName].hooks += 1;
        cef.hooks[eventName] = customEventMap[eventName].hooks;
        window.addEventListener(eventName, eventHook);
    };
    cef.removeEventListener = (eventName, eventHook) => {
        if (customEventMap[eventName] === undefined) {
            console.error(`window.${sdkModuleName}.addEventListener(eventName, eventHook) : eventName 必须是 ${Object.keys(customEventMap)} 中的一个`)
            return;
        }
        if (typeof eventHook !== 'function') {
            console.error(`window.${sdkModuleName}.addEventListener(eventName, eventHook): eventHook 必须是一个函数`);
            return;
        }
        customEventMap[eventName].hooks -= 1;
        cef.hooks[eventName] = customEventMap[eventName].hooks;
        window.removeEventListener(eventName, eventHook);
    };
    cef.show = (cid) => {
        if (window[moduleName] && typeof window[moduleName]['show_window'] === 'function') {
            window[moduleName]['show_window'](cid);
        }
    };
    cef.hide = (cid) => {
        if (window[moduleName] && typeof window[moduleName]['hide_window'] === 'function') {
            window[moduleName]['hide_window'](cid);
        }
    };
    cef.open = (params) => {
        if (window[moduleName] && typeof window[moduleName].open === 'function') {
            window[moduleName].open(params);
        }
    };
    cef.close = (cidLists) => {
        if (cidLists && Object.prototype.toString.call(cidLists) === '[object Array]') {
            if (window[moduleName] && typeof window[moduleName]['close_window'] === 'function') {
                window[moduleName]['close_window'](cidLists);
            }
        } else if (!cidLists) {
            if (window[moduleName] && typeof window[moduleName]['close_window'] === 'function') {
                window[moduleName]['close_window']();
            }
        } else {
            console.warn('__cef__.close(cidLists): cidLists 的值只能为 undefined 或者 array')
        }
    };
    cef.closeAll = () => {
        if (window[moduleName] && typeof window[moduleName]['close_all_window'] === 'function') {
            window[moduleName]['close_all_window']();
        }
    };
    cef.toggleFullScreen = () => {
        if (window[moduleName] && typeof window[moduleName]['toggle_full_screen'] === 'function') {
            window[moduleName]['toggle_full_screen']();
        }
    };
    cef.maximize = (uid) => {
        if (typeof uid === 'string') {
            if (window[moduleName] && typeof window[moduleName]['maximize_window'] === 'function') {
                window[moduleName]['maximize_window'](uid);
            }
        } else {
            if (window[moduleName] && typeof window[moduleName]['maximize_current_window'] === 'function') {
                window[moduleName]['maximize_current_window']();
            }
        }
    };
    cef.minimize = (uid) => {
        if (typeof uid === 'string') {
            if (window[moduleName] && typeof window[moduleName]['minimize_window'] === 'function') {
                window[moduleName]['minimize_window'](uid);
            }
        } else {
            if (window[moduleName] && typeof window[moduleName]['minimize_current_window'] === 'function') {
                window[moduleName]['minimize_current_window']();
            }
        }
    };
    cef.focus = (cid) => {
        if (window[moduleName] && typeof window[moduleName]['focus_browser'] === 'function') {
            window[moduleName]['focus_browser'](cid);
        }
    };
    cef.arouse = (cid) => {
        if (window[moduleName] && typeof window[moduleName]['arouse_window'] === 'function') {
            window[moduleName]['arouse_window'](cid);
        }
    };
    cef.setBrowserPayload = (cid, payload) => {
        if (typeof cid !== 'string' || cid === '') {
            console.error('__cef__.setBrowserPayload(cid ,payload): cid 必须为字符类型，且不为空字符串');
            return;
        }
        if (Object.prototype.toString.call(payload) !== '[object Object]') {
            console.error('__cef__.setBrowserPayload(cid ,payload): payload 必须为JsonObject');
            return;
        }
        if (window[moduleName] && typeof window[moduleName]['set_browser_payload'] === 'function') {
            window[moduleName]['set_browser_payload'](cid, payload);
        }

    };
    cef.broadCast = (eventData) => {
        if (eventData && Object.prototype.toString.call(eventData) !== '[object Object]') {
            console.error('__cef__.broadCast(eventData): eventData 为非必填项，如果传值，必须为Json Object');
            return;
        }
        if (window[moduleName] && typeof window[moduleName]['dispatch_customize_event'] === 'function') {
            window[moduleName]['dispatch_customize_event'](customEventMap.windowBroadcastEvent.name, eventData || {});
        }
    };
    cef.nestFrame = (params) => {
        if (params && Object.prototype.toString.call(params) !== '[object Object]') {
            console.error('__cef__.nestFrame(params): params 为非必填项，如果传值，必须为Json Object');
            return;
        }
        if (window[moduleName] && typeof window[moduleName]['nest_frame_window'] === 'function') {
            window[moduleName]['nest_frame_window'](params);
        }
    };
    cef.nestApplication = (params) => {
        if (!params || (params && Object.prototype.toString.call(params) !== '[object Object]')) {
            console.error('__cef__.nestApplication(params): params必须为Json Object');
            return;
        }
        if (window[moduleName] && typeof window[moduleName]['nest_third_party_application'] === 'function') {
            window[moduleName]['nest_third_party_application'](params);
        }
    };
    cef.refreshWindowGeometry = (cid) => {
        if (window[moduleName] && typeof window[moduleName]['update_window_geometry'] === 'function') {
            window[moduleName]['update_window_geometry'](cid);
        }
    };
    cef.showCloseDialog = (params) => {
        if (!params || (params && Object.prototype.toString.call(params) !== '[object Object]')) {
            console.error('__cef__.showCloseDialog(params): params必须为Json Object');
            return;
        }
        if (window[moduleName] && typeof window[moduleName]['show_close_dialog'] === 'function') {
            window[moduleName]['show_close_dialog'](params);
        }
    };
    cef.encryption = (code) => {
        return btoa(`${btoa(encryptionKey)}${btoa(code)}`)
    };
    cef.decryption = (code) => {
      const t_1 = atob(code);
      const t_2 = t_1.replace(btoa(encryptionKey), '');
      return atob(t_2);
    };
    cef.closeNestClient = (cid) => {
        if (window[moduleName] && typeof window[moduleName]['close_nest_client'] === 'function') {
            window[moduleName]['close_nest_client'](cid);
        }
    };
    cef.throwKeyEvent = (params) => {
        if (!params || (params && Object.prototype.toString.call(params) !== '[object Object]')) {
            console.error('__cef__.throwKeyEvent(params): params必须为Json Object');
            return;
        }
        if (window[moduleName] && typeof window[moduleName]['send_key_event_to_client'] === 'function') {
            window[moduleName]['send_key_event_to_client'](params);
        }
    };
    cef.setCurrentMenu = (params) => {
        if (params && Object.prototype.toString.call(params) === '[object String]') {
            window[moduleName]['set_menu_info'](params);
        }
    };
    cef.getCurrentMenu = () => {
        window[moduleName]['get_menu_info']();
    };
    cef.virtualEvents = (selector,obj) => {
        class KeyEvent {
        // 初始化
            init(Input,obj){
                this.Input = Input;
                this.vm=obj||{};
                this.value=[];
                let self = this;
                if (this.Input===null || this.Input===undefined  || this.Input.nodeName.toLocaleUpperCase() !== 'INPUT') {
                    return false;
                }
                this.Input.addEventListener('input', (e) => {
                         console.log(e);
                        if(/[\u4e00-\u9fa5]/.test(this.Input.value)!==true){
                             this.value=this.Input.value;
                        }
                });
                 this.Input.addEventListener('compositionend', (e) =>{
                       this.Input.value=this.value;
                 }, false);
            }
        };

       const _Key = new KeyEvent();
       return _Key.init(selector,obj);
    };
    cef.CEF_INFO = {};
    window[sdkModuleName] = cef;
    window[pythonCallBack] = python_cef;
    window.CEF_HAS_INITIALIZED = true;
}());"""
