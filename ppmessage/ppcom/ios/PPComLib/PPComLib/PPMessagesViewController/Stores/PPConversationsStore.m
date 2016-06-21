//
//  PPConversationsStore.m
//  PPComLib
//
//  Created by PPMessage on 4/1/16.
//  Copyright © 2016 Yvertical. All rights reserved.
//

#import "PPConversationsStore.h"

#import "PPAppInfo.h"
#import "PPMessage.h"
#import "PPConversationItem.h"

#import "PPFastLog.h"
#import "PPComUtils.h"

#import "PPGetConversationListHttpModel.h"
#import "PPGetAppOrgGroupListHttpModel.h"
#import "PPCreateConversationHttpModel.h"
#import "PPGetDefaultConversationHttpModels.h"

#define PP_ENABLE_LOG 1

@interface PPConversationsStore ()

@property (nonatomic) NSMutableArray *conversationItems;
@property (nonatomic) PPCom *client;
@property (nonatomic) BOOL fetchedFromServer; // 是否从服务器下载过conversation_list

@property (nonatomic) PPConversationItem *defaultConversation;

@end

@implementation PPConversationsStore

+ (instancetype)storeWithClient:(PPCom*)client {
    return [[self alloc] initWithClient:client];
}

- (instancetype)initWithClient:(PPCom*)client {
    if (self = [super init]) {
        self.conversationItems = [NSMutableArray array];
        self.client = client;
    }
    return self;
}

- (void)setWithConversations:(NSArray *)conversations {
    if (conversations && conversations.count > 0) {
        self.conversationItems = [NSMutableArray arrayWithArray:conversations];
    }
}

- (void)addConversation:(PPConversationItem *)conversation {
    if (conversation) {
        if (conversation.conversationItemType == PPConversationItemTypeGroup) {
            [self.conversationItems addObject:conversation];
        } else {
            NSInteger existIndex = [self indexForConversation:conversation.uuid];
            if (existIndex != NSNotFound) {
                PPConversationItem *exitConversationItem = [self.conversationItems objectAtIndex:existIndex];
                
                conversation.userName = PPIsNotNull(conversation.userName) ? conversation.userName : exitConversationItem.userName;
                conversation.messageSummary = PPIsNotNull(conversation.messageSummary) ? conversation.messageSummary : exitConversationItem.messageSummary;
                
                [self.conversationItems replaceObjectAtIndex:existIndex withObject:conversation];
                
            } else {
                [self.conversationItems addObject:conversation];
            }
        }
    }
}

- (void)addDefaultConversation:(PPConversationItem *)defaultConversation {
    self.defaultConversation = defaultConversation;
    [self addConversation:defaultConversation];
}

- (NSArray*)sortedConversations {
    return [self.conversationItems sortedArrayUsingComparator:^NSComparisonResult(PPConversationItem *obj1, PPConversationItem *obj2) {
        return [obj1 compare:obj2];
    }];
}

- (void)sortedConversationsWithBlock:(void (^)(NSArray *, NSError *))block {
    if (self.conversationItems && self.conversationItems.count > 0 && self.fetchedFromServer) {
        if (PP_ENABLE_LOG) PPFastLog(@"Find conversations from memory");
        if (block) block([self sortedConversations], nil);
        return;
    }
    
    // 1. get app orggroup
    [self getAppOrgGroupsWithBlock:^(id obj, NSDictionary *response, NSError *error) {
        
        NSMutableArray *conversations = obj ? obj : self.conversationItems;
        
        // 2. get conversations
        PPGetConversationListHttpModel *getConversationsTask = [PPGetConversationListHttpModel modelWithClient:self.client];
        [getConversationsTask getConversationListWithBlock:^(id obj, NSDictionary *response, NSError *error) {
            
            self.fetchedFromServer = YES;
            
            if (obj) {
                [conversations addObjectsFromArray:obj];
                [self addConversations:conversations];
            }
            
            if (block) block([self sortedConversations], error);
            
        }];
        
    }];
    
}

- (void)updateConversationsWithMessage:(PPMessage *)message {
    PPConversationItem *conversationItem = [PPConversationItem itemWithClient:self.client withMessageBody:message];
    NSInteger conversationIndex = [self indexForConversation:conversationItem.uuid];
    if (conversationIndex == NSNotFound) {
        [self.conversationItems addObject:conversationItem];
    } else {
        PPConversationItem *conversationItem = self.conversationItems[conversationIndex];
        conversationItem.messageSummary = [PPMessage summaryInMessage:message];
        conversationItem.messageTimestamp = message.timestamp;
    }
}

- (void)asyncFindConversationWithGroupUUID:(NSString *)groupUUID
                            completedBlock:(void (^)(PPConversationItem *, BOOL))completed {
    
    // Find group conversation from local
    NSInteger findIndex = [self indexForGroupConversation:groupUUID];
    if (findIndex != NSNotFound) {
        if (completed) completed(self.conversationItems[findIndex], YES);
        return;
    }
    
    // find from server
    PPCreateConversationHttpModel *createConversationTask = [PPCreateConversationHttpModel modelWithClient:self.client];
    [createConversationTask createWithGroupUUID:groupUUID completed:^(id obj, NSDictionary *response, NSError *error) {
        
        if (obj) {
            [self addConversation:obj];
        }
        
        if (completed) completed(obj, obj != nil);
        
    }];
    
}

- (void)findConversationAssociatedWithUserUUID:(NSString *)userUUID
                                 findCompleted:(void (^)(PPConversationItem *, BOOL))completedBlock {
    
    // Find from memory
    NSInteger findIndex = [self indexForAssignedUserConversation:userUUID];
    if (findIndex != NSNotFound) {
        if (completedBlock) completedBlock(self.conversationItems[findIndex], YES);
        return;
    }
    
    // find from server
    PPCreateConversationHttpModel *createConversationTask = [PPCreateConversationHttpModel modelWithClient:self.client];
    [createConversationTask createWithUserUUID:userUUID completed:^(id obj, NSDictionary *response, NSError *error) {
        
        if (obj) {
            [self addConversation:obj];
        }
        
        if (completedBlock) completedBlock(obj, obj != nil);
        
    }];
    
}

- (void)asyncGetDefaultConversationWithCompletedBlock:(void (^)(PPConversationItem *))completedBlock {
    if ([self isDefaultConversationAvaliable]) {
        if (completedBlock) completedBlock(self.defaultConversation);
        return;
    }
    
    PPGetDefaultConversationHttpModels *fetchDefaultConversation = [PPGetDefaultConversationHttpModels modelWithClient:self.client];
    [fetchDefaultConversation requestWithBlock:^(PPConversationItem *conversation, NSDictionary *response, NSError *error) {
        if (conversation) {
            [self addConversation:conversation];
            self.defaultConversation = conversation;
        }
        if (completedBlock) completedBlock(self.defaultConversation);
    }];
}

- (BOOL)isDefaultConversationAvaliable {
    return self.defaultConversation != nil;
}

#pragma mark - Helper

- (void)getAppOrgGroupsWithBlock:(PPHttpModelCompletedBlock)completedBlock {
    // Only show groups when `app_route_policy === GROUP`
    if (![self.client.appInfo.groupPolicy isEqualToString:PPAppInfoGroupPolicyGROUP]) {
        if (completedBlock) {
            completedBlock([NSMutableArray array], nil, nil);
        }
        return;
    }
    
    PPGetAppOrgGroupListHttpModel *getAppOrgGroupsTask = [PPGetAppOrgGroupListHttpModel modelWithClient:self.client];
    [getAppOrgGroupsTask getAppOrgGroupListWithBlock:completedBlock];
}

- (NSInteger)indexForConversation:(NSString*)conversationUUID {
    __block NSInteger findIndex = NSNotFound;
    if (self.conversationItems && self.conversationItems.count > 0) {
        [self.conversationItems enumerateObjectsUsingBlock:^(id  _Nonnull obj, NSUInteger idx, BOOL * _Nonnull stop) {
            PPConversationItem *conversationItem = obj;
            
            if ((conversationItem.conversationItemType != PPConversationItemTypeGroup) &&
                [conversationItem.uuid isEqualToString:conversationUUID]) {
                findIndex = idx;
                *stop = YES;
            }
            
        }];
    }
    return findIndex;
}

- (NSInteger)indexForGroupConversation:(NSString*)groupUUID {
    __block NSInteger findIndex = NSNotFound;
    if (self.conversationItems && self.conversationItems.count > 0) {
        [self.conversationItems enumerateObjectsUsingBlock:^(id  _Nonnull obj, NSUInteger idx, BOOL * _Nonnull stop) {
            PPConversationItem *conversationItem = obj;
            if (conversationItem.conversationItemType != PPConversationItemTypeGroup &&
                PPIsNotNull(conversationItem.groupUUID) &&
                [conversationItem.groupUUID isEqualToString:groupUUID]) {
                findIndex = idx;
                *stop = YES;
            }
        }];
    }
    return findIndex;
}

- (NSInteger)indexForAssignedUserConversation:(NSString*)userUUID {
    __block NSInteger findIndex = NSNotFound;
    if (self.conversationItems && self.conversationItems.count > 0) {
        [self.conversationItems enumerateObjectsUsingBlock:^(id  _Nonnull obj, NSUInteger idx, BOOL * _Nonnull stop) {
            PPConversationItem *conversationItem = obj;
            if (PPIsNotNull(conversationItem.assignedUUID) && [conversationItem.assignedUUID isEqualToString:userUUID]) {
                findIndex = idx;
                *stop = YES;
            }
        }];
    }
    return findIndex;
}

- (BOOL)isConversationExit:(NSString*)conversationoUUID {
    return [self indexForConversation:conversationoUUID] != NSNotFound;
}

- (void)addConversations:(NSMutableArray*)conversations {
    if (conversations && conversations.count > 0) {
        [conversations enumerateObjectsUsingBlock:^(id  _Nonnull obj, NSUInteger idx, BOOL * _Nonnull stop) {
            [self addConversation:obj];
        }];
    }
}

@end
