//
//  PPGetConversationInfoHttpModel.h
//  PPComLib
//
//  Created by PPMessage on 5/5/16.
//  Copyright © 2016 Yvertical. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "PPHttpModel.h"

@class PPCom;

@interface PPGetConversationInfoHttpModel : NSObject

- (instancetype)initWithClient:(PPCom*)client;

- (void)getWithConversationUUID:(NSString*)conversationUUID
                 completedBlock:(PPHttpModelCompletedBlock)completedBlock;

@end
