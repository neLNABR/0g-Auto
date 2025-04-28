ALL_TASKS_INFO = {
    "operationName": "CampaignActivitiesPanel",
    "variables": {
        "campaignId": "f7e24f14-b911-4f11-b903-edac89a095ec",
        "isTrusted": True,
    },
    "query": "fragment ActivityFields on CampaignActivity {\n  id\n  createdAt\n  updatedAt\n  startDateTimeAt\n  endDateTimeAt\n  title\n  description\n  coverAssetUrl\n  type\n  identityType\n  recurringPeriod {\n    count\n    type\n    __typename\n  }\n  recurringMaxCount\n  properties\n  records {\n    id\n    status\n    createdAt\n    activityId\n    properties\n    rewardRecords {\n      id\n      status\n      appliedRewardType\n      appliedRewardQuantity\n      appliedRewardMetadata\n      error\n      rewardId\n      reward {\n        id\n        quantity\n        type\n        properties\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  tags {\n    id\n    name\n    __typename\n  }\n  reward {\n    id\n    title\n    description\n    quantity\n    type\n    imageUrl\n    properties\n    __typename\n  }\n  targetReward {\n    id\n    activityId\n    missionId\n    __typename\n  }\n  nft {\n    id\n    tokenId\n    name\n    description\n    image\n    properties\n    mintPrice\n    platformFee\n    maxSupply\n    maxMintCountPerAddress\n    nftContract {\n      id\n      address\n      type\n      chainId\n      __typename\n    }\n    __typename\n  }\n  isHidden\n  __typename\n}\n\nfragment MissionFields on CampaignMission {\n  id\n  createdAt\n  updatedAt\n  startDateTimeAt\n  endDateTimeAt\n  title\n  description\n  coverPhotoUrl\n  recurringPeriod {\n    count\n    type\n    __typename\n  }\n  recurringMaxCount\n  properties\n  tags {\n    id\n    name\n    __typename\n  }\n  rewards {\n    id\n    title\n    description\n    quantity\n    type\n    imageUrl\n    properties\n    awardMechanism\n    __typename\n  }\n  records {\n    id\n    status\n    createdAt\n    missionId\n    rewardRecords {\n      id\n      status\n      appliedRewardType\n      appliedRewardQuantity\n      appliedRewardMetadata\n      error\n      rewardId\n      reward {\n        id\n        quantity\n        type\n        properties\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  activities {\n    id\n    __typename\n  }\n  isHidden\n  __typename\n}\n\nfragment CampaignCommunityGoalFields on CampaignCommunityGoal {\n  id\n  title\n  description\n  additionalDetails\n  imageUrl\n  threshold\n  status\n  startDateTimeAt\n  endDateTimeAt\n  createdAt\n  updatedAt\n  isThresholdHidden\n  isHidden\n  ctaButtonCopy\n  ctaButtonUrl\n  __typename\n}\n\nquery CampaignActivitiesPanel($campaignId: String!) {\n  campaign(id: $campaignId) {\n    activities {\n      ...ActivityFields\n      __typename\n    }\n    missions {\n      ...MissionFields\n      __typename\n    }\n    communityGoals {\n      ...CampaignCommunityGoalFields\n      activity {\n        ...ActivityFields\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

FOLLOW_MICHAEL_HEINRICH_CEO_0G_LABS = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "1cd50bdf-fe19-424d-8d92-744f0ff9ace1"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

FOLLOW_MING_WU_CEO_0G_LABS = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "fd912f44-772e-4919-826e-b2bd5fa93e02"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}


FOLLOW_0G_FOUNDATION = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "67b20482-57e2-4ed4-a5fc-88ff66a8559d"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

FOLLOW_0G_LABS = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "6bbd5c7e-ad18-4274-8a9c-ed26a4f047f3"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

FOLLOW_ONE_GRAVITY_THE_FIRST_NFT_COLLECTION_ON_0G = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "9673d2ce-c6c8-441e-b420-09ea82a39a6e"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

FOLLOW_AI_VERSE_COMING_SOON = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "9be09897-1eba-4cd4-98c0-f39c0a56600f"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

FOLLOW_BATTLE_OF_AGENTS_COMING_SOON = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "95ea2d98-147b-4683-b5c7-a76d3f43af47"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

DAILY_CHECK_IN = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "c35c81a8-b46b-427a-b1f6-f30a1a65691d"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

USER_INFO = {
    "operationName": "UserMe",
    "variables": {"campaignId": "f7e24f14-b911-4f11-b903-edac89a095ec"},
    "query": "fragment RecordFields on CampaignSpot {\n  records {\n    id\n    status\n    properties\n    points\n    instanceCount\n    createdAt\n    updatedAt\n    activityId\n    activity {\n      id\n      title\n      description\n      type\n      __typename\n    }\n    mission {\n      id\n      title\n      description\n      __typename\n    }\n    communityGoal {\n      id\n      title\n      description\n      threshold\n      __typename\n    }\n    rewardRecords {\n      id\n      status\n      appliedRewardType\n      appliedRewardQuantity\n      appliedRewardMetadata\n      error\n      rewardId\n      reward {\n        id\n        quantity\n        type\n        properties\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery UserMe($campaignId: String!) {\n  userMe {\n    id\n    campaignSpot(campaignId: $campaignId) {\n      id\n      points\n      referralCode\n      referralCodeEditsRemaining\n      ...RecordFields\n      __typename\n    }\n    __typename\n  }\n}",
}

LIKE_HYPE_UP_GUILD_ON_0G_PROJECTS = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "63e1a820-8747-42f4-a37c-451270500902"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

RT_HYPE_UP_GUILD_ON_0G_PROJECTS = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "4c127fe8-2f72-4ed5-b7e1-0dafc10325ec"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

LIKE_SUPPORT_ONE_GRAVITY = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "2e8d513e-128b-4d6f-8b37-273968d08020"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

RT_SUPPORT_ONE_GRAVITY = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "abd62a3f-843e-43ae-a837-d8488e6debf3"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

LIKE_YOU_NEED_DECENTRALIZED_AI = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "f957f392-9006-4376-a4e7-898933881489"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

RT_YOU_NEED_DECENTRALIZED_AI = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "897bd4de-d0fb-479e-a98f-75090f0bed38"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

LIKE_BATTLE_OF_AGENTS_IS_COMING_SOON = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "e40b782b-995d-4bc7-b29c-530cd1ed8842"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

RT_BATTLE_OF_AGENTS_IS_COMING_SOON = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "b18526f3-4858-44ff-86ee-470b896464d0"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

LIKE_GUILD_ON_0G_WITH_MICHAEL = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "c5de2a7c-ca1e-49a0-8995-8646f6557a27"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

RT_GUILD_ON_0G_WITH_MICHAEL = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "5f5bae28-0dea-484d-a487-957f184e3507"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

LIKE_LEARN_FROM_MING = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "40d47589-217f-46e4-993a-2c88a7e5ed8e"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

RT_LEARN_FROM_MING = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "5dc5ff35-753f-490a-8d4b-5555b44bc74a"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

LIKE_600K_STRONG_ON_X = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "c64e56dc-7d98-4eb6-afa0-32944cfa3ef8"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

RT_600K_STRONG_ON_X = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "db434aa4-f98d-4cb6-aca7-49029f7af754"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}


FOLLOW_ADA_HEINRICH_MD_CMO_0G_LABS = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "2c8af9a5-28dc-4faf-962c-529f5fd31203"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

LIKE_0G_IN_KOREA = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "cd0584f2-b457-4276-89b0-780fb0eed68e"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

RT_0G_IN_KOREA = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "c6ff4b78-2b3d-4b2e-85ce-e27c2669e3fb"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

LIKE_TECH_UPDATES = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "284e976b-7d37-4963-8909-8c05d8d15e75"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

RT_TECH_UPDATES = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "388b2df8-1771-475a-a30e-6d9f0d8bfe78"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

LIKE_WHAT_S_YOUR_DREAM_AI_BATTLE = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "dc477441-8cc3-4b58-beaf-4dae02dfb2a2"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

RT_WHAT_S_YOUR_DREAM_AI_BATTLE = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "0a972489-90c1-42b3-8b4d-263573bad2a8"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

LIKE_EARLY_ACCESS_SOON = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "bf4bc88b-d733-4272-92a3-e23b111b62e5"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

RT_EARLY_ACCESS_SOON = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "7218de61-2dd5-4724-85db-2f5a61549bca"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

LIKE_300K_PUZZLE_SOLVERS = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "7615839e-59d5-4087-a97f-e1f62bc78beb"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

RT_300K_PUZZLE_SOLVERS = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "b5b4b2a3-1905-4449-ab84-9120bbbc1fbc"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

LIKE_0G_HUB = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "20294e3f-9181-46de-b59e-82b910bc32be"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

RT_0G_HUB = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "aa136d10-9974-479e-8a4d-57f5eaf8e645"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}

FOLLLOW_0G_CN = {
    "operationName": "VerifyActivity",
    "variables": {"data": {"activityId": "e020d2cb-140c-416f-95e3-2766aa74697c"}},
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
}


def get_verify_activity(activity_id: str = None) -> dict:
    return {
        "operationName": "VerifyActivity",
        "variables": {"data": {"activityId": activity_id}},
        "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
    }


def get_verify_activity_json(referral_code: str = None) -> dict:
    return {
        "operationName": "VerifyActivity",
        "variables": {
            "data": {
                "activityId": "8cdc0521-90c1-435e-b108-78761eb9e60a",
                "metadata": {"referralCode": referral_code},
            }
        },
        "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
    }
