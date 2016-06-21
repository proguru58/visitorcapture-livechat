//
//  PPStoreManager.h
//  PPComLib
//
//  Created by PPMessage on 4/1/16.
//  Copyright © 2016 Yvertical. All rights reserved.
//

#import <Foundation/Foundation.h>

@class PPConversationsStore, PPMessagesStore, PPGroupMembersStore, PPCom;

@interface PPStoreManager : NSObject

+ (instancetype)instanceWithClient:(PPCom*)client;

@property (nonatomic) PPConversationsStore *conversationStore;
@property (nonatomic) PPMessagesStore *messagesStore;
@property (nonatomic) PPGroupMembersStore *groupMembersStore;

@end
