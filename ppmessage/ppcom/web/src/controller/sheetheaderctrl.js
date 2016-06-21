Ctrl.$sheetheader = (function() {

    var $device = Service.$device;

    return {
        onSheetHeaderInit: onSheetHeaderInit,
        
        getHeaderTitle: getHeaderTitle,
        onSheetHeaderClicked: onSheetHeaderClicked,
        setHeaderTitle: setHeaderTitle,
        
        minimize: minimize,
        closed: closed,
        
        incrUnread: incrUnread,
        decrUnread: decrUnread,
    }

    ///////// Implenmentation ///////
    function minimize() {

        // We disable body scroll when user click launcher in mobile browser,
        // So we need to enable it again when the user press minimize button
        // @see `launcherctrl.js` `showMessageBox` methods
        if ($device.isIOS()) {
            $device.enableScroll();
        }

        View.$launcher.showLauncher();
        View.$conversation.hide();

        // Cancel all sechedule tasks
        Service.$schedule.cancelAll();
        Service.$sheetHeader.close(false);

        cancelAnyWaitingToCreateConversations();

    }

    function getHeaderTitle() {
        return Service.$sheetHeader.getHeaderTitle();
    }

    function onSheetHeaderClicked() {
        Ctrl.$emojiSelector.get().showSelector(false);
    }

    function setHeaderTitle(title) {
        title = title || getHeaderTitle();
        Service.$sheetHeader.setHeaderTitle(title);
        View.$sheetHeader.setTitle(title);
    }

    function closed() {
        return Service.$sheetHeader.closed();
    }

    function onSheetHeaderInit() {
        Service.$sheetHeader.asyncGetHeaderTitle(function(title) {
            setHeaderTitle(title);
        });

        // decide should show group button, when app init
        Service.$conversationManager.asyncGetList( function( conversationList ) {

            var len = ( conversationList || [] ).length;
            // more than one conversations, so show `conversations` button in the sheetHeader
            if ( len > 1 ) {
                View.$sheetHeader.showGroupButton();
            }
            
        } );
        
    }

    function incrUnread() {
        Service.$sheetHeader.incrUnreadCount();
        View.$sheetHeader.setUnreadCount(Service.$sheetHeader.unreadCount());
    }

    function decrUnread( count ) {
        Service.$sheetHeader.decrUnreadCount ( count );
        View.$sheetHeader.setUnreadCount(Service.$sheetHeader.unreadCount());
    }

    function cancelAnyWaitingToCreateConversations() {
        var $conversationAgency = Service.$conversationAgency,
            inRequestingGroupConversation = $conversationAgency.isRequestingGroupConversation(),
            DELAY_TIME = 300; // Waiting the css animation completed

        Ctrl.$conversationPanel.stopPollingWaitingQueueLength();
        $timeout( function() {
            setHeaderTitle();
            // resume to `MODE.LIST` mode if we are waiting group conversations
            inRequestingGroupConversation && Ctrl.$conversationList.show();
            // resume to `MODE.CONTENT` mode if we are waiting default conversations
            !$conversationAgency.isDefaultConversationAvaliable() &&
                Ctrl.$conversationPanel.mode( Ctrl.$conversationPanel.MODE.CONTENT );
        }, DELAY_TIME );
    }
    
})();
