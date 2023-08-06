# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Wrappers for protocol buffer enum types."""

import enum


class TrackingCodePageFormatEnum(object):
    class TrackingCodePageFormat(enum.IntEnum):
        """
        The format of the web page where the tracking tag and snippet will be
        installed.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          HTML (int): Standard HTML page format.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        HTML = 2


class TrackingCodeTypeEnum(object):
    class TrackingCodeType(enum.IntEnum):
        """
        The type of the generated tag snippets for tracking conversions.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          WEBPAGE (int): The snippet that is fired as a result of a website page loading.
          WEBPAGE_ONCLICK (int): The snippet contains a JavaScript function which fires the tag. This
          function is typically called from an onClick handler added to a link or
          button element on the page.
          CLICK_TO_CALL (int): For embedding on a mobile webpage. The snippet contains a JavaScript
          function which fires the tag.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        WEBPAGE = 2
        WEBPAGE_ONCLICK = 3
        CLICK_TO_CALL = 4


class CallConversionReportingStateEnum(object):
    class CallConversionReportingState(enum.IntEnum):
        """
        Possible data types for a call conversion action state.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          DISABLED (int): Call conversion action is disabled.
          USE_ACCOUNT_LEVEL_CALL_CONVERSION_ACTION (int): Call conversion action will use call conversion type set at the
          account level.
          USE_RESOURCE_LEVEL_CALL_CONVERSION_ACTION (int): Call conversion action will use call conversion type set at the resource
          (call only ads/call extensions) level.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DISABLED = 2
        USE_ACCOUNT_LEVEL_CALL_CONVERSION_ACTION = 3
        USE_RESOURCE_LEVEL_CALL_CONVERSION_ACTION = 4


class DisplayAdFormatSettingEnum(object):
    class DisplayAdFormatSetting(enum.IntEnum):
        """
        Enumerates display ad format settings.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The value is unknown in this version.
          ALL_FORMATS (int): Text, image and native formats.
          NON_NATIVE (int): Text and image formats.
          NATIVE (int): Native format, i.e. the format rendering is controlled by the publisher
          and not by Google.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ALL_FORMATS = 2
        NON_NATIVE = 3
        NATIVE = 4


class PageOnePromotedStrategyGoalEnum(object):
    class PageOnePromotedStrategyGoal(enum.IntEnum):
        """
        Enum describing possible strategy goals.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          FIRST_PAGE (int): First page on google.com.
          FIRST_PAGE_PROMOTED (int): Top slots of the first page on google.com.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        FIRST_PAGE = 2
        FIRST_PAGE_PROMOTED = 3


class PolicyTopicEntryTypeEnum(object):
    class PolicyTopicEntryType(enum.IntEnum):
        """
        The possible policy topic entry types.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          PROHIBITED (int): The resource will not be served.
          LIMITED (int): The resource will not be served under some circumstances.
          DESCRIPTIVE (int): May be of interest, but does not limit how the resource is served.
          BROADENING (int): Could increase coverage beyond normal.
          AREA_OF_INTEREST_ONLY (int): Constrained for all targeted countries, but may serve in other countries
          through area of interest.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        PROHIBITED = 2
        LIMITED = 4
        DESCRIPTIVE = 5
        BROADENING = 6
        AREA_OF_INTEREST_ONLY = 7


class PolicyTopicEvidenceDestinationMismatchUrlTypeEnum(object):
    class PolicyTopicEvidenceDestinationMismatchUrlType(enum.IntEnum):
        """
        The possible policy topic evidence destination mismatch url types.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          DISPLAY_URL (int): The display url.
          FINAL_URL (int): The final url.
          FINAL_MOBILE_URL (int): The final mobile url.
          TRACKING_URL (int): The tracking url template, with substituted desktop url.
          MOBILE_TRACKING_URL (int): The tracking url template, with substituted mobile url.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DISPLAY_URL = 2
        FINAL_URL = 3
        FINAL_MOBILE_URL = 4
        TRACKING_URL = 5
        MOBILE_TRACKING_URL = 6


class AgeRangeTypeEnum(object):
    class AgeRangeType(enum.IntEnum):
        """
        The type of demographic age ranges (e.g. between 18 and 24 years old).

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          AGE_RANGE_18_24 (int): Between 18 and 24 years old.
          AGE_RANGE_25_34 (int): Between 25 and 34 years old.
          AGE_RANGE_35_44 (int): Between 35 and 44 years old.
          AGE_RANGE_45_54 (int): Between 45 and 54 years old.
          AGE_RANGE_55_64 (int): Between 55 and 64 years old.
          AGE_RANGE_65_UP (int): 65 years old and beyond.
          AGE_RANGE_UNDETERMINED (int): Undetermined age range.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        AGE_RANGE_18_24 = 503001
        AGE_RANGE_25_34 = 503002
        AGE_RANGE_35_44 = 503003
        AGE_RANGE_45_54 = 503004
        AGE_RANGE_55_64 = 503005
        AGE_RANGE_65_UP = 503006
        AGE_RANGE_UNDETERMINED = 503999


class DayOfWeekEnum(object):
    class DayOfWeek(enum.IntEnum):
        """
        Enumerates days of the week, e.g., \"Monday\".

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The value is unknown in this version.
          MONDAY (int): Monday.
          TUESDAY (int): Tuesday.
          WEDNESDAY (int): Wednesday.
          THURSDAY (int): Thursday.
          FRIDAY (int): Friday.
          SATURDAY (int): Saturday.
          SUNDAY (int): Sunday.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        MONDAY = 2
        TUESDAY = 3
        WEDNESDAY = 4
        THURSDAY = 5
        FRIDAY = 6
        SATURDAY = 7
        SUNDAY = 8


class DeviceEnum(object):
    class Device(enum.IntEnum):
        """
        Enumerates Google Ads devices available for targeting.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The value is unknown in this version.
          MOBILE (int): Mobile devices with full browsers.
          TABLET (int): Tablets with full browsers.
          DESKTOP (int): Computers.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        MOBILE = 2
        TABLET = 3
        DESKTOP = 4


class GenderTypeEnum(object):
    class GenderType(enum.IntEnum):
        """
        The type of demographic genders (e.g. female).

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          MALE (int): Male.
          FEMALE (int): Female.
          UNDETERMINED (int): Undetermined gender.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        MALE = 10
        FEMALE = 11
        UNDETERMINED = 20


class HotelDateSelectionTypeEnum(object):
    class HotelDateSelectionType(enum.IntEnum):
        """
        Enum describing possible hotel date selection types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          DEFAULT_SELECTION (int): Dates selected by default.
          USER_SELECTED (int): Dates selected by the user.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DEFAULT_SELECTION = 50
        USER_SELECTED = 51


class IncomeRangeTypeEnum(object):
    class IncomeRangeType(enum.IntEnum):
        """
        The type of demographic income ranges (e.g. between 0% to 50%).

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          INCOME_RANGE_0_50 (int): 0%-50%.
          INCOME_RANGE_50_60 (int): 50% to 60%.
          INCOME_RANGE_60_70 (int): 60% to 70%.
          INCOME_RANGE_70_80 (int): 70% to 80%.
          INCOME_RANGE_80_90 (int): 80% to 90%.
          INCOME_RANGE_90_UP (int): Greater than 90%.
          INCOME_RANGE_UNDETERMINED (int): Undetermined income range.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INCOME_RANGE_0_50 = 510001
        INCOME_RANGE_50_60 = 510002
        INCOME_RANGE_60_70 = 510003
        INCOME_RANGE_70_80 = 510004
        INCOME_RANGE_80_90 = 510005
        INCOME_RANGE_90_UP = 510006
        INCOME_RANGE_UNDETERMINED = 510000


class InteractionTypeEnum(object):
    class InteractionType(enum.IntEnum):
        """
        Enum describing possible interaction types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          CALLS (int): Calls.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CALLS = 8000


class KeywordMatchTypeEnum(object):
    class KeywordMatchType(enum.IntEnum):
        """
        Possible Keyword match types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          EXACT (int): Exact match.
          PHRASE (int): Phrase match.
          BROAD (int): Broad match.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        EXACT = 2
        PHRASE = 3
        BROAD = 4


class ListingCustomAttributeIndexEnum(object):
    class ListingCustomAttributeIndex(enum.IntEnum):
        """
        The index of the listing custom attribute.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          CUSTOM_ATTRIBUTE_0 (int): First listing custom attribute.
          CUSTOM_ATTRIBUTE_1 (int): Second listing custom attribute.
          CUSTOM_ATTRIBUTE_2 (int): Third listing custom attribute.
          CUSTOM_ATTRIBUTE_3 (int): Fourth listing custom attribute.
          CUSTOM_ATTRIBUTE_4 (int): Fifth listing custom attribute.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CUSTOM_ATTRIBUTE_0 = 2
        CUSTOM_ATTRIBUTE_1 = 3
        CUSTOM_ATTRIBUTE_2 = 4
        CUSTOM_ATTRIBUTE_3 = 5
        CUSTOM_ATTRIBUTE_4 = 6


class ListingGroupTypeEnum(object):
    class ListingGroupType(enum.IntEnum):
        """
        The type of the listing group.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          SUBDIVISION (int): Subdivision of products along some listing dimension. These nodes
          are not used by serving to target listing entries, but is purely
          to define the structure of the tree.
          UNIT (int): Listing group unit that defines a bid.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        SUBDIVISION = 2
        UNIT = 3


class MinuteOfHourEnum(object):
    class MinuteOfHour(enum.IntEnum):
        """
        Enumerates of quarter-hours. E.g. \"FIFTEEN\"

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The value is unknown in this version.
          ZERO (int): Zero minutes past the hour.
          FIFTEEN (int): Fifteen minutes past the hour.
          THIRTY (int): Thirty minutes past the hour.
          FORTY_FIVE (int): Forty-five minutes past the hour.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ZERO = 2
        FIFTEEN = 3
        THIRTY = 4
        FORTY_FIVE = 5


class ParentalStatusTypeEnum(object):
    class ParentalStatusType(enum.IntEnum):
        """
        The type of parental statuses (e.g. not a parent).

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          PARENT (int): Parent.
          NOT_A_PARENT (int): Not a parent.
          UNDETERMINED (int): Undetermined parental status.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        PARENT = 300
        NOT_A_PARENT = 301
        UNDETERMINED = 302


class ProductChannelEnum(object):
    class ProductChannel(enum.IntEnum):
        """
        Enum describing the locality of a product offer.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ONLINE (int): The item is sold online.
          LOCAL (int): The item is sold in local stores.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ONLINE = 2
        LOCAL = 3


class ProductChannelExclusivityEnum(object):
    class ProductChannelExclusivity(enum.IntEnum):
        """
        Enum describing the availability of a product offer.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          SINGLE_CHANNEL (int): The item is sold through one channel only, either local stores or online
          as indicated by its ProductChannel.
          MULTI_CHANNEL (int): The item is matched to its online or local stores counterpart, indicating
          it is available for purchase in both ShoppingProductChannels.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        SINGLE_CHANNEL = 2
        MULTI_CHANNEL = 3


class ProductConditionEnum(object):
    class ProductCondition(enum.IntEnum):
        """
        Enum describing the condition of a product offer.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          OLD (int): The product condition is old.
          NEW (int): The product condition is new.
          REFURBISHED (int): The product condition is refurbished.
          USED (int): The product condition is used.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        OLD = 2
        NEW = 3
        REFURBISHED = 4
        USED = 5


class ProductTypeLevelEnum(object):
    class ProductTypeLevel(enum.IntEnum):
        """
        Enum describing the level of the type of a product offer.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          PRODUCT_TYPE_L1 (int): Level 1.
          PRODUCT_TYPE_L2 (int): Level 2.
          PRODUCT_TYPE_L3 (int): Level 3.
          PRODUCT_TYPE_L4 (int): Level 4.
          PRODUCT_TYPE_L5 (int): Level 5.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        PRODUCT_TYPE_L1 = 2
        PRODUCT_TYPE_L2 = 3
        PRODUCT_TYPE_L3 = 4
        PRODUCT_TYPE_L4 = 5
        PRODUCT_TYPE_L5 = 6


class ProximityRadiusUnitsEnum(object):
    class ProximityRadiusUnits(enum.IntEnum):
        """
        The unit of radius distance in proximity (e.g. MILES)

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          MILES (int): Miles
          KILOMETERS (int): Kilometers
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        MILES = 2
        KILOMETERS = 3


class AdServingOptimizationStatusEnum(object):
    class AdServingOptimizationStatus(enum.IntEnum):
        """
        Enum describing possible serving statuses.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          OPTIMIZE (int): Ad serving is optimized based on CTR for the campaign.
          CONVERSION_OPTIMIZE (int): Ad serving is optimized based on CTR * Conversion for the campaign. If
          the campaign is not in the conversion optimizer bidding strategy, it will
          default to OPTIMIZED.
          ROTATE (int): Ads are rotated evenly for 90 days, then optimized for clicks.
          ROTATE_INDEFINITELY (int): Show lower performing ads more evenly with higher performing ads, and do
          not optimize.
          UNAVAILABLE (int): Ad serving optimization status is not available.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        OPTIMIZE = 2
        CONVERSION_OPTIMIZE = 3
        ROTATE = 4
        ROTATE_INDEFINITELY = 5
        UNAVAILABLE = 6


class TargetCpaOptInRecommendationGoalEnum(object):
    class TargetCpaOptInRecommendationGoal(enum.IntEnum):
        """
        Goal of TargetCpaOptIn recommendation.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          SAME_COST (int): Recommendation to set Target CPA to maintain the same cost.
          SAME_CONVERSIONS (int): Recommendation to set Target CPA to maintain the same conversions.
          SAME_CPA (int): Recommendation to set Target CPA to maintain the same CPA.
          CLOSEST_CPA (int): Recommendation to set Target CPA to a value that is as close as possible
          to, yet lower than, the actual CPA (computed for past 28 days).
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        SAME_COST = 2
        SAME_CONVERSIONS = 3
        SAME_CPA = 4
        CLOSEST_CPA = 5


class BiddingStrategyTypeEnum(object):
    class BiddingStrategyType(enum.IntEnum):
        """
        Enum describing possible bidding strategy types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ENHANCED_CPC (int): Enhanced CPC is a bidding strategy that raises bids for clicks
          that seem more likely to lead to a conversion and lowers
          them for clicks where they seem less likely.
          MANUAL_CPC (int): Manual click based bidding where user pays per click.
          MANUAL_CPM (int): Manual impression based bidding
          where user pays per thousand impressions.
          MANUAL_CPV (int): A bidding strategy that pays a configurable amount per video view.
          MAXIMIZE_CONVERSIONS (int): A bidding strategy that automatically maximizes number of conversions
          given a daily budget.
          MAXIMIZE_CONVERSION_VALUE (int): An automated bidding strategy that automatically sets bids to maximize
          revenue while spending your budget.
          PAGE_ONE_PROMOTED (int): Page-One Promoted bidding scheme, which sets max cpc bids to
          target impressions on page one or page one promoted slots on google.com.
          PERCENT_CPC (int): Percent Cpc is bidding strategy where bids are a fraction of the
          advertised price for some good or service.
          TARGET_CPA (int): Target CPA is an automated bid strategy that sets bids
          to help get as many conversions as possible
          at the target cost-per-acquisition (CPA) you set.
          TARGET_OUTRANK_SHARE (int): Target Outrank Share is an automated bidding strategy that sets bids
          based on the target fraction of auctions where the advertiser
          should outrank a specific competitor.
          TARGET_ROAS (int): Target ROAS is an automated bidding strategy
          that helps you maximize revenue while averaging
          a specific target Return On Average Spend (ROAS).
          TARGET_SPEND (int): Target Spend is an automated bid strategy that sets your bids
          to help get as many clicks as possible within your budget.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENHANCED_CPC = 2
        MANUAL_CPC = 3
        MANUAL_CPM = 4
        MANUAL_CPV = 13
        MAXIMIZE_CONVERSIONS = 10
        MAXIMIZE_CONVERSION_VALUE = 11
        PAGE_ONE_PROMOTED = 5
        PERCENT_CPC = 12
        TARGET_CPA = 6
        TARGET_OUTRANK_SHARE = 7
        TARGET_ROAS = 8
        TARGET_SPEND = 9


class CampaignGroupStatusEnum(object):
    class CampaignGroupStatus(enum.IntEnum):
        """
        Possible statuses of a CampaignGroup.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ENABLED (int): Campaign group is currently serving ads depending on budget information.
          REMOVED (int): Campaign group has been removed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        REMOVED = 4


class GeoTargetConstantStatusEnum(object):
    class GeoTargetConstantStatus(enum.IntEnum):
        """
        The possible statuses of a geo target constant.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          ENABLED (int): The geo target constant is valid.
          REMOVAL_PLANNED (int): The geo target constant is obsolete and will be removed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        REMOVAL_PLANNED = 3


class CampaignServingStatusEnum(object):
    class CampaignServingStatus(enum.IntEnum):
        """
        Possible serving statuses of a campaign.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          SERVING (int): Serving.
          NONE (int): None.
          ENDED (int): Ended.
          PENDING (int): Pending.
          SUSPENDED (int): Suspended.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        SERVING = 2
        NONE = 3
        ENDED = 4
        PENDING = 5
        SUSPENDED = 6


class ChangeStatusResourceTypeEnum(object):
    class ChangeStatusResourceType(enum.IntEnum):
        """
        Enum listing the resource types support by the ChangeStatus resource.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): Used for return value only. Represents an unclassified resource unknown
          in this version.
          AD_GROUP (int): An AdGroup resource change.
          AD_GROUP_AD (int): An AdGroupAd resource change.
          AD_GROUP_CRITERION (int): An AdGroupCriterion resource change.
          CAMPAIGN (int): A Campaign resource change.
          CAMPAIGN_CRITERION (int): A CampaignCriterion resource change.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        AD_GROUP = 3
        AD_GROUP_AD = 4
        AD_GROUP_CRITERION = 5
        CAMPAIGN = 6
        CAMPAIGN_CRITERION = 7


class QualityScoreBucketEnum(object):
    class QualityScoreBucket(enum.IntEnum):
        """
        Enum listing the possible quality score buckets.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          BELOW_AVERAGE (int): Quality of the creative is below average.
          AVERAGE (int): Quality of the creative is average.
          ABOVE_AVERAGE (int): Quality of the creative is above average.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        BELOW_AVERAGE = 2
        AVERAGE = 3
        ABOVE_AVERAGE = 4


class AdGroupStatusEnum(object):
    class AdGroupStatus(enum.IntEnum):
        """
        The possible statuses of an ad group.

        Attributes:
          UNSPECIFIED (int): The status has not been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          ENABLED (int): The ad group is enabled.
          PAUSED (int): The ad group is paused.
          REMOVED (int): The ad group is removed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        PAUSED = 3
        REMOVED = 4


class GoogleAdsFieldDataTypeEnum(object):
    class GoogleAdsFieldDataType(enum.IntEnum):
        """
        These are the various types a GoogleAdsService artifact may take on.

        Attributes:
          UNSPECIFIED (int): Unspecified
          UNKNOWN (int): Unknown
          BOOLEAN (int): Maps to google.protobuf.BoolValue

          Applicable operators:  =, !=
          DATE (int): Maps to google.protobuf.StringValue. It can be compared using the set of
          operators specific to dates however.

          Applicable operators:  =, <, >, <=, >=, BETWEEN, DURING, and IN
          DOUBLE (int): Maps to google.protobuf.DoubleValue

          Applicable operators:  =, !=, <, >, IN, NOT IN
          ENUM (int): Maps to an enum. It's specific definition can be found at type_url.

          Applicable operators:  =, !=, IN, NOT IN
          FLOAT (int): Maps to google.protobuf.FloatValue

          Applicable operators:  =, !=, <, >, IN, NOT IN
          INT32 (int): Maps to google.protobuf.Int32Value

          Applicable operators:  =, !=, <, >, <=, >=, BETWEEN, IN, NOT IN
          INT64 (int): Maps to google.protobuf.Int64Value

          Applicable operators:  =, !=, <, >, <=, >=, BETWEEN, IN, NOT IN
          MESSAGE (int): Maps to a protocol buffer message type. The data type's details can be
          found in type_url.

          No operators work with MESSAGE fields.
          RESOURCE_NAME (int): Maps to google.protobuf.StringValue. Represents the resource name
          (unique id) of a resource or one of its foreign keys.

          No operators work with RESOURCE_NAME fields.
          STRING (int): Maps to google.protobuf.StringValue.

          Applicable operators:  =, !=, LIKE, NOT LIKE, IN, NOT IN
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        BOOLEAN = 2
        DATE = 3
        DOUBLE = 4
        ENUM = 5
        FLOAT = 6
        INT32 = 7
        INT64 = 8
        MESSAGE = 9
        RESOURCE_NAME = 10
        STRING = 11


class MimeTypeEnum(object):
    class MimeType(enum.IntEnum):
        """
        The mime type

        Attributes:
          UNSPECIFIED (int): The mime type has not been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          IMAGE_JPEG (int): MIME type of image/jpeg.
          IMAGE_GIF (int): MIME type of image/gif.
          IMAGE_PNG (int): MIME type of image/png.
          FLASH (int): MIME type of application/x-shockwave-flash.
          TEXT_HTML (int): MIME type of text/html.
          PDF (int): MIME type of application/pdf.
          MSWORD (int): MIME type of application/msword.
          MSEXCEL (int): MIME type of application/vnd.ms-excel.
          RTF (int): MIME type of application/rtf.
          AUDIO_WAV (int): MIME type of audio/wav.
          AUDIO_MP3 (int): MIME type of audio/mp3.
          HTML5_AD_ZIP (int): MIME type of application/x-html5-ad-zip.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        IMAGE_JPEG = 2
        IMAGE_GIF = 3
        IMAGE_PNG = 4
        FLASH = 5
        TEXT_HTML = 6
        PDF = 7
        MSWORD = 8
        MSEXCEL = 9
        RTF = 10
        AUDIO_WAV = 11
        AUDIO_MP3 = 12
        HTML5_AD_ZIP = 13


class TimeTypeEnum(object):
    class TimeType(enum.IntEnum):
        """
        The possible time types used by certain resources as an alternative to
        absolute timestamps.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          NOW (int): As soon as possible.
          FOREVER (int): An infinite point in the future.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        NOW = 2
        FOREVER = 3


class BudgetStatusEnum(object):
    class BudgetStatus(enum.IntEnum):
        """
        Possible statuses of a Budget.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ENABLED (int): Budget is enabled.
          REMOVED (int): Budget is removed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        REMOVED = 3


class AdGroupCriterionStatusEnum(object):
    class AdGroupCriterionStatus(enum.IntEnum):
        """
        The possible statuses of an AdGroupCriterion.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          ENABLED (int): The ad group criterion is enabled.
          PAUSED (int): The ad group criterion is paused.
          REMOVED (int): The ad group criterion is removed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        PAUSED = 3
        REMOVED = 4


class CampaignSharedSetStatusEnum(object):
    class CampaignSharedSetStatus(enum.IntEnum):
        """
        Enum listing the possible campaign shared set statuses.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ENABLED (int): The campaign shared set is enabled.
          REMOVED (int): The campaign shared set is removed and can no longer be used.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        REMOVED = 3


class AttributionModelEnum(object):
    class AttributionModel(enum.IntEnum):
        """
        The attribution model that describes how to distribute credit for a
        particular conversion across potentially many prior interactions.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          EXTERNAL (int): Uses external attribution.
          GOOGLE_ADS_LAST_CLICK (int): Attributes all credit for a conversion to its last click.
          GOOGLE_SEARCH_ATTRIBUTION_FIRST_CLICK (int): Attributes all credit for a conversion to its first click using Google
          Search attribution.
          GOOGLE_SEARCH_ATTRIBUTION_LINEAR (int): Attributes credit for a conversion equally across all of its clicks using
          Google Search attribution.
          GOOGLE_SEARCH_ATTRIBUTION_TIME_DECAY (int): Attributes exponentially more credit for a conversion to its more recent
          clicks using Google Search attribution (half-life is 1 week).
          GOOGLE_SEARCH_ATTRIBUTION_POSITION_BASED (int): Attributes 40% of the credit for a conversion to its first and last
          clicks. Remaining 20% is evenly distributed across all other clicks. This
          uses Google Search attribution.
          GOOGLE_SEARCH_ATTRIBUTION_DATA_DRIVEN (int): Flexible model that uses machine learning to determine the appropriate
          distribution of credit among clicks using Google Search attribution.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        EXTERNAL = 100
        GOOGLE_ADS_LAST_CLICK = 101
        GOOGLE_SEARCH_ATTRIBUTION_FIRST_CLICK = 102
        GOOGLE_SEARCH_ATTRIBUTION_LINEAR = 103
        GOOGLE_SEARCH_ATTRIBUTION_TIME_DECAY = 104
        GOOGLE_SEARCH_ATTRIBUTION_POSITION_BASED = 105
        GOOGLE_SEARCH_ATTRIBUTION_DATA_DRIVEN = 106


class AccountBudgetProposalStatusEnum(object):
    class AccountBudgetProposalStatus(enum.IntEnum):
        """
        The possible statuses of an AccountBudgetProposal.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          PENDING (int): The proposal is pending approval.
          APPROVED_HELD (int): The proposal has been approved but the corresponding billing setup
          has not.  This can occur for proposals that set up the first budget
          when signing up for billing or when performing a change of bill-to
          operation.
          APPROVED (int): The proposal has been approved.
          CANCELLED (int): The proposal has been cancelled by the user.
          REJECTED (int): The proposal has been rejected by the user, e.g. by rejecting an
          acceptance email.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        PENDING = 2
        APPROVED_HELD = 3
        APPROVED = 4
        CANCELLED = 5
        REJECTED = 6


class SlotEnum(object):
    class Slot(enum.IntEnum):
        """
        Enumerates possible positions of the Ad.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The value is unknown in this version.
          SEARCH_SIDE (int): Google search: Side.
          SEARCH_TOP (int): Google search: Top.
          SEARCH_OTHER (int): Google search: Other.
          CONTENT (int): Google Display Network.
          SEARCH_PARTNER_TOP (int): Search partners: Top.
          SEARCH_PARTNER_OTHER (int): Search partners: Other.
          MIXED (int): Cross-network.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        SEARCH_SIDE = 2
        SEARCH_TOP = 3
        SEARCH_OTHER = 4
        CONTENT = 5
        SEARCH_PARTNER_TOP = 6
        SEARCH_PARTNER_OTHER = 7
        MIXED = 8


class CampaignStatusEnum(object):
    class CampaignStatus(enum.IntEnum):
        """
        Possible statuses of a campaign.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ENABLED (int): Campaign is currently serving ads depending on budget information.
          PAUSED (int): Campaign has been paused by the user.
          REMOVED (int): Campaign has been removed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        PAUSED = 3
        REMOVED = 4


class MonthOfYearEnum(object):
    class MonthOfYear(enum.IntEnum):
        """
        Enumerates months of the year, e.g., \"January\".

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The value is unknown in this version.
          JANUARY (int): January.
          FEBRUARY (int): February.
          MARCH (int): March.
          APRIL (int): April.
          MAY (int): May.
          JUNE (int): June.
          JULY (int): July.
          AUGUST (int): August.
          SEPTEMBER (int): September.
          OCTOBER (int): October.
          NOVEMBER (int): November.
          DECEMBER (int): December.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        JANUARY = 2
        FEBRUARY = 3
        MARCH = 4
        APRIL = 5
        MAY = 6
        JUNE = 7
        JULY = 8
        AUGUST = 9
        SEPTEMBER = 10
        OCTOBER = 11
        NOVEMBER = 12
        DECEMBER = 13


class ConversionActionCategoryEnum(object):
    class ConversionActionCategory(enum.IntEnum):
        """
        The category of conversions that are associated with a ConversionAction.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          DEFAULT (int): Default category.
          PAGE_VIEW (int): User visiting a page.
          PURCHASE (int): Purchase, sales, or \"order placed\" event.
          SIGNUP (int): Signup user action.
          LEAD (int): Lead-generating action.
          DOWNLOAD (int): Software download action (as for an app).
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DEFAULT = 2
        PAGE_VIEW = 3
        PURCHASE = 4
        SIGNUP = 5
        LEAD = 6
        DOWNLOAD = 7


class PolicyApprovalStatusEnum(object):
    class PolicyApprovalStatus(enum.IntEnum):
        """
        The possible policy approval statuses. When there are several approval
        statuses available the most severe one will be used. The order of severity
        is DISAPPROVED, AREA_OF_INTEREST_ONLY, APPROVED_LIMITED and APPROVED.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          DISAPPROVED (int): Will not serve.
          APPROVED_LIMITED (int): Serves with restrictions.
          APPROVED (int): Serves without restrictions.
          AREA_OF_INTEREST_ONLY (int): Will not serve in targeted countries, but may serve for users who are
          searching for information about the targeted countries.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DISAPPROVED = 2
        APPROVED_LIMITED = 3
        APPROVED = 4
        AREA_OF_INTEREST_ONLY = 5


class ConversionActionTypeEnum(object):
    class ConversionActionType(enum.IntEnum):
        """
        Possible types of a conversion action.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          AD_CALL (int): Conversions that occur when a user clicks on an ad's call extension.
          CLICK_TO_CALL (int): Conversions that occur when a user on a mobile device clicks a phone
          number.
          GOOGLE_PLAY_DOWNLOAD (int): Conversions that occur when a user downloads a mobile app from the Google
          Play Store.
          GOOGLE_PLAY_IN_APP_PURCHASE (int): Conversions that occur when a user makes a purchase in an app through
          Android billing.
          UPLOAD_CALLS (int): Call conversions that are tracked by the advertiser and uploaded.
          UPLOAD_CLICKS (int): Conversions that are tracked by the advertiser and uploaded with
          attributed clicks.
          WEBPAGE (int): Conversions that occur on a webpage.
          WEBSITE_CALL (int): Conversions that occur when a user calls a dynamically-generated phone
          number from an advertiser's website.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        AD_CALL = 2
        CLICK_TO_CALL = 3
        GOOGLE_PLAY_DOWNLOAD = 4
        GOOGLE_PLAY_IN_APP_PURCHASE = 5
        UPLOAD_CALLS = 6
        UPLOAD_CLICKS = 7
        WEBPAGE = 8
        WEBSITE_CALL = 9


class BiddingSourceEnum(object):
    class BiddingSource(enum.IntEnum):
        """
        Enum describing possible bidding sources.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ADGROUP (int): Bidding entity is defined on the ad group.
          CRITERION (int): Bidding entity is defined on the ad group criterion.
          CAMPAIGN_BIDDING_STRATEGY (int): Effective bidding entity is inherited from campaign bidding strategy.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ADGROUP = 2
        CRITERION = 3
        CAMPAIGN_BIDDING_STRATEGY = 5


class BudgetDeliveryMethodEnum(object):
    class BudgetDeliveryMethod(enum.IntEnum):
        """
        Possible delivery methods of a Budget.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          STANDARD (int): The budget server will throttle serving evenly across
          the entire time period.
          ACCELERATED (int): The budget server will not throttle serving,
          and ads will serve as fast as possible.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        STANDARD = 2
        ACCELERATED = 3


class RecommendationTypeEnum(object):
    class RecommendationType(enum.IntEnum):
        """
        Types of recommendations.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          CAMPAIGN_BUDGET (int): Budget recommendation for budget constrained campaigns.
          KEYWORD (int): Keyword recommendation.
          TEXT_AD (int): Recommendation to add a new text ad.
          TARGET_CPA_OPT_IN (int): Recommendation to update a campaign to use a Target CPA bidding strategy.
          MAXIMIZE_CONVERSIONS_OPT_IN (int): Recommendation to update a campaign to use the Maximize Conversions
          bidding strategy.
          ENHANCED_CPC_OPT_IN (int): Recommendation to enable Enhanced Cost Per Click for a campaign.
          SEARCH_PARTNERS_OPT_IN (int): Recommendation to start showing your campaign's ads on Google Search
          Partners Websites.
          MAXIMIZE_CLICKS_OPT_IN (int): Recommendation to update a campaign to use a Maximize Clicks bidding
          strategy.
          OPTIMIZE_AD_ROTATION (int): Recommendation to start using the \"Optimize\" ad rotation setting for the
          given ad group.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CAMPAIGN_BUDGET = 2
        KEYWORD = 3
        TEXT_AD = 4
        TARGET_CPA_OPT_IN = 5
        MAXIMIZE_CONVERSIONS_OPT_IN = 6
        ENHANCED_CPC_OPT_IN = 7
        SEARCH_PARTNERS_OPT_IN = 8
        MAXIMIZE_CLICKS_OPT_IN = 9
        OPTIMIZE_AD_ROTATION = 10


class GoogleAdsFieldCategoryEnum(object):
    class GoogleAdsFieldCategory(enum.IntEnum):
        """
        The category of the artifact.

        Attributes:
          UNSPECIFIED (int): Unspecified
          UNKNOWN (int): Unknown
          RESOURCE (int): The described artifact is a resource.
          ATTRIBUTE (int): The described artifact is a field and is an attribute of a resource.
          Including a resource attribute field in a query may segment the query if
          the resource to which it is attributed segments the resource found in
          the FROM clause.
          SEGMENT (int): The described artifact is a field and always segments search queries.
          METRIC (int): The described artifact is a field and is a metric. It never segments
          search queries.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        RESOURCE = 2
        ATTRIBUTE = 3
        SEGMENT = 5
        METRIC = 6


class SharedSetStatusEnum(object):
    class SharedSetStatus(enum.IntEnum):
        """
        Enum listing the possible shared set statuses.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ENABLED (int): The shared set is enabled.
          REMOVED (int): The shared set is removed and can no longer be used.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        REMOVED = 3


class AccountBudgetProposalTypeEnum(object):
    class AccountBudgetProposalType(enum.IntEnum):
        """
        The possible types of an AccountBudgetProposal.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          CREATE (int): Identifies a request to create a new budget.
          UPDATE (int): Identifies a request to edit an existing budget.
          END (int): Identifies a request to end a budget that has already started.
          REMOVE (int): Identifies a request to remove a budget that hasn't started yet.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CREATE = 2
        UPDATE = 3
        END = 4
        REMOVE = 5


class ConversionActionStatusEnum(object):
    class ConversionActionStatus(enum.IntEnum):
        """
        Possible statuses of a conversion action.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ENABLED (int): Conversions will be recorded.
          REMOVED (int): Conversions will not be recorded.
          HIDDEN (int): Conversions will not be recorded and the conversion action will not
          appear in the UI.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        REMOVED = 3
        HIDDEN = 4


class BillingSetupStatusEnum(object):
    class BillingSetupStatus(enum.IntEnum):
        """
        The possible statuses of a BillingSetup.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          PENDING (int): The billing setup is pending approval.
          APPROVED_HELD (int): The billing setup has been approved but the corresponding first budget
          has not.  This can only occur for billing setups configured for monthly
          invoicing.
          APPROVED (int): The billing setup has been approved.
          CANCELLED (int): The billing setup was cancelled by the user prior to approval.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        PENDING = 2
        APPROVED_HELD = 3
        APPROVED = 4
        CANCELLED = 5


class SharedSetTypeEnum(object):
    class SharedSetType(enum.IntEnum):
        """
        Enum listing the possible shared set types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          NEGATIVE_KEYWORDS (int): A set of keywords that can be excluded from targeting.
          NEGATIVE_PLACEMENTS (int): A set of placements that can be excluded from targeting.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        NEGATIVE_KEYWORDS = 2
        NEGATIVE_PLACEMENTS = 3


class CriterionTypeEnum(object):
    class CriterionType(enum.IntEnum):
        """
        Enum describing possible criterion types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          KEYWORD (int): Keyword. e.g. 'mars cruise'.
          PLACEMENT (int): Placement, aka Website. e.g. 'www.flowers4sale.com'
          DEVICE (int): Devices to target.
          LOCATION (int): Locations to target.
          LISTING_GROUP (int): Listing groups to target.
          AD_SCHEDULE (int): Ad Schedule.
          AGE_RANGE (int): Age range.
          GENDER (int): Gender.
          INCOME_RANGE (int): Income Range.
          PARENTAL_STATUS (int): Parental status.
          YOUTUBE_VIDEO (int): YouTube Video.
          YOUTUBE_CHANNEL (int): YouTube Channel.
          PROXIMITY (int): Proximity.
          TOPIC (int): A topic target on the content network (e.g. \"Pets & Animals\").
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        KEYWORD = 2
        PLACEMENT = 3
        DEVICE = 6
        LOCATION = 7
        LISTING_GROUP = 8
        AD_SCHEDULE = 9
        AGE_RANGE = 10
        GENDER = 11
        INCOME_RANGE = 12
        PARENTAL_STATUS = 13
        YOUTUBE_VIDEO = 14
        YOUTUBE_CHANNEL = 15
        PROXIMITY = 17
        TOPIC = 18


class PolicyReviewStatusEnum(object):
    class PolicyReviewStatus(enum.IntEnum):
        """
        The possible policy review statuses.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          REVIEW_IN_PROGRESS (int): Currently under review.
          REVIEWED (int): Primary review complete. Other reviews may be continuing.
          UNDER_APPEAL (int): The resource has been resubmitted for approval or its policy decision has
          been appealed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        REVIEW_IN_PROGRESS = 2
        REVIEWED = 3
        UNDER_APPEAL = 4


class AdTypeEnum(object):
    class AdType(enum.IntEnum):
        """
        The possible types of an ad.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          TEXT_AD (int): The ad is a text ad.
          EXPANDED_TEXT_AD (int): The ad is an expanded text ad.
          DYNAMIC_SEARCH_AD (int): The ad is a dynamic search ad.
          RESPONSIVE_DISPLAY_AD (int): The ad is a responsive display ad.
          CALL_ONLY_AD (int): The ad is a call only ad.
          EXPANDED_DYNAMIC_SEARCH_AD (int): The ad is an expanded dynamic search ad.
          HOTEL_AD (int): The ad is a hotel ad.
          SHOPPING_SMART_AD (int): The ad is a Smart Shopping ad.
          SHOPPING_PRODUCT_AD (int): The ad is a standard Shopping ad.
          VIDEO_OUTSTREAM (int): Video outstream ad.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        TEXT_AD = 2
        EXPANDED_TEXT_AD = 3
        DYNAMIC_SEARCH_AD = 4
        RESPONSIVE_DISPLAY_AD = 5
        CALL_ONLY_AD = 6
        EXPANDED_DYNAMIC_SEARCH_AD = 7
        HOTEL_AD = 8
        SHOPPING_SMART_AD = 9
        SHOPPING_PRODUCT_AD = 10
        VIDEO_OUTSTREAM = 11


class AdGroupTypeEnum(object):
    class AdGroupType(enum.IntEnum):
        """
        Enum listing the possible types of an ad group.

        Attributes:
          UNSPECIFIED (int): The type has not been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          SEARCH_STANDARD (int): The default ad group type for Search campaigns.
          DISPLAY_STANDARD (int): The default ad group type for Display campaigns.
          SHOPPING_PRODUCT_ADS (int): The ad group type for Shopping campaigns serving standard product ads.
          HOTEL_ADS (int): The default ad group type for Hotel campaigns.
          SHOPPING_SMART_ADS (int): The type for ad groups in Smart Shopping campaigns.
          VIDEO_BUMPER (int): Short unskippable in-stream video ads.
          VIDEO_TRUE_VIEW_IN_STREAM (int): TrueView (skippable) in-stream video ads.
          VIDEO_TRUE_VIEW_IN_DISPLAY (int): TrueView in-display video ads.
          VIDEO_NON_SKIPPABLE_IN_STREAM (int): Unskippable in-stream video ads.
          VIDEO_OUTSTREAM (int): Outstream video ads.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        SEARCH_STANDARD = 2
        DISPLAY_STANDARD = 3
        SHOPPING_PRODUCT_ADS = 4
        HOTEL_ADS = 6
        SHOPPING_SMART_ADS = 7
        VIDEO_BUMPER = 8
        VIDEO_TRUE_VIEW_IN_STREAM = 9
        VIDEO_TRUE_VIEW_IN_DISPLAY = 10
        VIDEO_NON_SKIPPABLE_IN_STREAM = 11
        VIDEO_OUTSTREAM = 12


class ConversionActionCountingTypeEnum(object):
    class ConversionActionCountingType(enum.IntEnum):
        """
        Indicates how conversions for this action will be counted. For more
        information, see https://support.google.com/google-ads/answer/3438531.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ONE_PER_CLICK (int): Count only one conversion per click.
          MANY_PER_CLICK (int): Count all conversions per click.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ONE_PER_CLICK = 2
        MANY_PER_CLICK = 3


class ManagerLinkStatusEnum(object):
    class ManagerLinkStatus(enum.IntEnum):
        """
        Possible statuses of a link.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          ACTIVE (int): Indicates current in-effect relationship
          INACTIVE (int): Indicates terminated relationship
          PENDING (int): Indicates relationship has been requested by manager, but the client
          hasn't accepted yet.
          REFUSED (int): Relationship was requested by the manager, but the client has refused.
          CANCELED (int): Indicates relationship has been requested by manager, but manager
          canceled it.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ACTIVE = 2
        INACTIVE = 3
        PENDING = 4
        REFUSED = 5
        CANCELED = 6


class AdGroupAdRotationModeEnum(object):
    class AdGroupAdRotationMode(enum.IntEnum):
        """
        The possible ad rotation modes of an ad group.

        Attributes:
          UNSPECIFIED (int): The ad rotation mode has not been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          OPTIMIZE (int): Optimize ad group ads based on clicks or conversions.
          ROTATE_FOREVER (int): Rotate evenly forever.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        OPTIMIZE = 2
        ROTATE_FOREVER = 3


class SpendingLimitTypeEnum(object):
    class SpendingLimitType(enum.IntEnum):
        """
        The possible spending limit types used by certain resources as an
        alternative to absolute money values in micros.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          INFINITE (int): Infinite, indicates unlimited spending power.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INFINITE = 2


class DataDrivenModelStatusEnum(object):
    class DataDrivenModelStatus(enum.IntEnum):
        """
        Enumerates data driven model statuses.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          AVAILABLE (int): The data driven model is available.
          STALE (int): The data driven model is stale. It hasn't been updated for at least 7
          days. It is still being used, but will become expired if it does not get
          updated for 30 days.
          EXPIRED (int): The data driven model expired. It hasn't been updated for at least 30
          days and cannot be used. Most commonly this is because there hasn't been
          the required number of events in a recent 30-day period.
          NEVER_GENERATED (int): The data driven model has never been generated. Most commonly this is
          because there has never been the required number of events in any 30-day
          period.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        AVAILABLE = 2
        STALE = 3
        EXPIRED = 4
        NEVER_GENERATED = 5


class ChangeStatusOperationEnum(object):
    class ChangeStatusOperation(enum.IntEnum):
        """
        Status of the changed resource

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): Used for return value only. Represents an unclassified resource unknown
          in this version.
          ADDED (int): The resource was created.
          CHANGED (int): The resource was modified.
          REMOVED (int): The resource was removed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ADDED = 2
        CHANGED = 3
        REMOVED = 4


class AdvertisingChannelSubTypeEnum(object):
    class AdvertisingChannelSubType(enum.IntEnum):
        """
        Enum describing the different channel subtypes.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used as a return value only. Represents value unknown in this version.
          SEARCH_MOBILE_APP (int): Mobile app campaigns for Search.
          DISPLAY_MOBILE_APP (int): Mobile app campaigns for Display.
          SEARCH_EXPRESS (int): AdWords express campaigns for search.
          DISPLAY_EXPRESS (int): AdWords Express campaigns for display.
          SHOPPING_SMART_ADS (int): Smart Shopping campaigns.
          DISPLAY_GMAIL_AD (int): Gmail Ad campaigns.
          DISPLAY_SMART_CAMPAIGN (int): Smart display campaigns.
          VIDEO_OUTSTREAM (int): Video Outstream campaigns.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        SEARCH_MOBILE_APP = 2
        DISPLAY_MOBILE_APP = 3
        SEARCH_EXPRESS = 4
        DISPLAY_EXPRESS = 5
        SHOPPING_SMART_ADS = 6
        DISPLAY_GMAIL_AD = 7
        DISPLAY_SMART_CAMPAIGN = 8
        VIDEO_OUTSTREAM = 9


class AdNetworkTypeEnum(object):
    class AdNetworkType(enum.IntEnum):
        """
        Enumerates Google Ads network types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): The value is unknown in this version.
          SEARCH (int): Google search.
          SEARCH_PARTNERS (int): Search partners.
          CONTENT (int): Display Network.
          YOUTUBE_SEARCH (int): YouTube Search.
          YOUTUBE_WATCH (int): YouTube Videos
          MIXED (int): Cross-network.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        SEARCH = 2
        SEARCH_PARTNERS = 3
        CONTENT = 4
        YOUTUBE_SEARCH = 5
        YOUTUBE_WATCH = 6
        MIXED = 7


class BidModifierSourceEnum(object):
    class BidModifierSource(enum.IntEnum):
        """
        Enum describing possible bid modifier sources.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          CAMPAIGN (int): The bid modifier is specified at the campaign level, on the campaign
          level criterion.
          AD_GROUP (int): The bid modifier is specified (overridden) at the ad group level.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CAMPAIGN = 2
        AD_GROUP = 3


class AccountBudgetStatusEnum(object):
    class AccountBudgetStatus(enum.IntEnum):
        """
        The possible statuses of an AccountBudget.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          PENDING (int): The account budget is pending approval.
          APPROVED (int): The account budget has been approved.
          CANCELLED (int): The account budget has been cancelled by the user.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        PENDING = 2
        APPROVED = 3
        CANCELLED = 4


class AdvertisingChannelTypeEnum(object):
    class AdvertisingChannelType(enum.IntEnum):
        """
        Enum describing the various advertising channel types.

        Attributes:
          UNSPECIFIED (int): Not specified.
          UNKNOWN (int): Used for return value only. Represents value unknown in this version.
          SEARCH (int): Search Network. Includes display bundled, and Search+ campaigns.
          DISPLAY (int): Google Display Network only.
          SHOPPING (int): Shopping campaigns serve on the shopping property
          and on google.com search results.
          HOTEL (int): Hotel Ads campaigns.
          VIDEO (int): Video campaigns.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        SEARCH = 2
        DISPLAY = 3
        SHOPPING = 4
        HOTEL = 5
        VIDEO = 6


class MediaTypeEnum(object):
    class MediaType(enum.IntEnum):
        """
        The type of media.

        Attributes:
          UNSPECIFIED (int): The media type has not been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          IMAGE (int): Static image, used for image ad.
          ICON (int): Small image, used for map ad.
          MEDIA_BUNDLE (int): ZIP file, used in fields of template ads.
          AUDIO (int): Audio file.
          VIDEO (int): Video file.
          DYNAMIC_IMAGE (int): Animated image, such as animated GIF.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        IMAGE = 2
        ICON = 3
        MEDIA_BUNDLE = 4
        AUDIO = 5
        VIDEO = 6
        DYNAMIC_IMAGE = 7


class AdGroupAdStatusEnum(object):
    class AdGroupAdStatus(enum.IntEnum):
        """
        The possible statuses of an AdGroupAd.

        Attributes:
          UNSPECIFIED (int): No value has been specified.
          UNKNOWN (int): The received value is not known in this version.

          This is a response-only value.
          ENABLED (int): The ad group ad is enabled.
          PAUSED (int): The ad group ad is paused.
          REMOVED (int): The ad group ad is removed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        PAUSED = 3
        REMOVED = 4


class AdGroupBidModifierErrorEnum(object):
    class AdGroupBidModifierError(enum.IntEnum):
        """
        Enum describing possible ad group bid modifier errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CRITERION_ID_NOT_SUPPORTED (int): The criterion ID does not support bid modification.
          CANNOT_OVERRIDE_OPTED_OUT_CAMPAIGN_CRITERION_BID_MODIFIER (int): Cannot override the bid modifier for the given criterion ID if the parent
          campaign is opted out of the same criterion.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CRITERION_ID_NOT_SUPPORTED = 2
        CANNOT_OVERRIDE_OPTED_OUT_CAMPAIGN_CRITERION_BID_MODIFIER = 3


class MediaBundleErrorEnum(object):
    class MediaBundleError(enum.IntEnum):
        """
        Enum describing possible media bundle errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          BAD_REQUEST (int): There was a problem with the request.
          DOUBLECLICK_BUNDLE_NOT_ALLOWED (int): HTML5 ads using DoubleClick Studio created ZIP files are not supported.
          EXTERNAL_URL_NOT_ALLOWED (int): Cannot reference URL external to the media bundle.
          FILE_TOO_LARGE (int): Media bundle file is too large.
          GOOGLE_WEB_DESIGNER_ZIP_FILE_NOT_PUBLISHED (int): ZIP file from Google Web Designer is not published.
          INVALID_INPUT (int): Input was invalid.
          INVALID_MEDIA_BUNDLE (int): There was a problem with the media bundle.
          INVALID_MEDIA_BUNDLE_ENTRY (int): There was a problem with one or more of the media bundle entries.
          INVALID_MIME_TYPE (int): The media bundle contains a file with an unknown mime type
          INVALID_PATH (int): The media bundle contain an invalid asset path.
          INVALID_URL_REFERENCE (int): HTML5 ad is trying to reference an asset not in .ZIP file
          MEDIA_DATA_TOO_LARGE (int): Media data is too large.
          MISSING_PRIMARY_MEDIA_BUNDLE_ENTRY (int): The media bundle contains no primary entry.
          SERVER_ERROR (int): There was an error on the server.
          STORAGE_ERROR (int): The image could not be stored.
          SWIFFY_BUNDLE_NOT_ALLOWED (int): Media bundle created with the Swiffy tool is not allowed.
          TOO_MANY_FILES (int): The media bundle contains too many files.
          UNEXPECTED_SIZE (int): The media bundle is not of legal dimensions.
          UNSUPPORTED_GOOGLE_WEB_DESIGNER_ENVIRONMENT (int): Google Web Designer not created for \"Google Ads\" environment.
          UNSUPPORTED_HTML5_FEATURE (int): Unsupported HTML5 feature in HTML5 asset.
          URL_IN_MEDIA_BUNDLE_NOT_SSL_COMPLIANT (int): URL in HTML5 entry is not ssl compliant.
          CUSTOM_EXIT_NOT_ALLOWED (int): Custom exits not allowed in HTML5 entry.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        BAD_REQUEST = 3
        DOUBLECLICK_BUNDLE_NOT_ALLOWED = 4
        EXTERNAL_URL_NOT_ALLOWED = 5
        FILE_TOO_LARGE = 6
        GOOGLE_WEB_DESIGNER_ZIP_FILE_NOT_PUBLISHED = 7
        INVALID_INPUT = 8
        INVALID_MEDIA_BUNDLE = 9
        INVALID_MEDIA_BUNDLE_ENTRY = 10
        INVALID_MIME_TYPE = 11
        INVALID_PATH = 12
        INVALID_URL_REFERENCE = 13
        MEDIA_DATA_TOO_LARGE = 14
        MISSING_PRIMARY_MEDIA_BUNDLE_ENTRY = 15
        SERVER_ERROR = 16
        STORAGE_ERROR = 17
        SWIFFY_BUNDLE_NOT_ALLOWED = 18
        TOO_MANY_FILES = 19
        UNEXPECTED_SIZE = 20
        UNSUPPORTED_GOOGLE_WEB_DESIGNER_ENVIRONMENT = 21
        UNSUPPORTED_HTML5_FEATURE = 22
        URL_IN_MEDIA_BUNDLE_NOT_SSL_COMPLIANT = 23
        CUSTOM_EXIT_NOT_ALLOWED = 24


class AdxErrorEnum(object):
    class AdxError(enum.IntEnum):
        """
        Enum describing possible adx errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          UNSUPPORTED_FEATURE (int): Attempt to use non-AdX feature by AdX customer.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        UNSUPPORTED_FEATURE = 2


class ListOperationErrorEnum(object):
    class ListOperationError(enum.IntEnum):
        """
        Enum describing possible list operation errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          REQUIRED_FIELD_MISSING (int): Field required in value is missing.
          DUPLICATE_VALUES (int): Duplicate or identical value is sent in multiple list operations.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        REQUIRED_FIELD_MISSING = 7
        DUPLICATE_VALUES = 8


class BiddingStrategyErrorEnum(object):
    class BiddingStrategyError(enum.IntEnum):
        """
        Enum describing possible bidding strategy errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          DUPLICATE_NAME (int): Each bidding strategy must have a unique name.
          CANNOT_CHANGE_BIDDING_STRATEGY_TYPE (int): Bidding strategy type is immutable.
          CANNOT_REMOVE_ASSOCIATED_STRATEGY (int): Only bidding strategies not linked to campaigns, adgroups or adgroup
          criteria can be removed.
          BIDDING_STRATEGY_NOT_SUPPORTED (int): The specified bidding strategy is not supported.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DUPLICATE_NAME = 2
        CANNOT_CHANGE_BIDDING_STRATEGY_TYPE = 3
        CANNOT_REMOVE_ASSOCIATED_STRATEGY = 4
        BIDDING_STRATEGY_NOT_SUPPORTED = 5


class EnumErrorEnum(object):
    class EnumError(enum.IntEnum):
        """
        Enum describing possible enum errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          ENUM_VALUE_NOT_PERMITTED (int): The enum value is not permitted.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENUM_VALUE_NOT_PERMITTED = 3


class RangeErrorEnum(object):
    class RangeError(enum.IntEnum):
        """
        Enum describing possible range errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          TOO_LOW (int): Too low.
          TOO_HIGH (int): Too high.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        TOO_LOW = 2
        TOO_HIGH = 3


class AdGroupErrorEnum(object):
    class AdGroupError(enum.IntEnum):
        """
        Enum describing possible ad group errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          DUPLICATE_ADGROUP_NAME (int): AdGroup with the same name already exists for the campaign.
          INVALID_ADGROUP_NAME (int): AdGroup name is not valid.
          ADVERTISER_NOT_ON_CONTENT_NETWORK (int): Advertiser is not allowed to target sites or set site bids that are not
          on the Google Search Network.
          BID_TOO_BIG (int): Bid amount is too big.
          BID_TYPE_AND_BIDDING_STRATEGY_MISMATCH (int): AdGroup bid does not match the campaign's bidding strategy.
          MISSING_ADGROUP_NAME (int): AdGroup name is required for Add.
          ADGROUP_LABEL_DOES_NOT_EXIST (int): No link found between the ad group and the label.
          ADGROUP_LABEL_ALREADY_EXISTS (int): The label has already been attached to the ad group.
          INVALID_CONTENT_BID_CRITERION_TYPE_GROUP (int): The CriterionTypeGroup is not supported for the content bid dimension.
          AD_GROUP_TYPE_NOT_VALID_FOR_ADVERTISING_CHANNEL_TYPE (int): The ad group type is not compatible with the campaign channel type.
          ADGROUP_TYPE_NOT_SUPPORTED_FOR_CAMPAIGN_SALES_COUNTRY (int): The ad group type is not supported in the country of sale of the
          campaign.
          CANNOT_ADD_ADGROUP_OF_TYPE_DSA_TO_CAMPAIGN_WITHOUT_DSA_SETTING (int): Ad groups of AdGroupType.SEARCH_DYNAMIC_ADS can only be added to
          campaigns that have DynamicSearchAdsSetting attached.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DUPLICATE_ADGROUP_NAME = 2
        INVALID_ADGROUP_NAME = 3
        ADVERTISER_NOT_ON_CONTENT_NETWORK = 5
        BID_TOO_BIG = 6
        BID_TYPE_AND_BIDDING_STRATEGY_MISMATCH = 7
        MISSING_ADGROUP_NAME = 8
        ADGROUP_LABEL_DOES_NOT_EXIST = 9
        ADGROUP_LABEL_ALREADY_EXISTS = 10
        INVALID_CONTENT_BID_CRITERION_TYPE_GROUP = 11
        AD_GROUP_TYPE_NOT_VALID_FOR_ADVERTISING_CHANNEL_TYPE = 12
        ADGROUP_TYPE_NOT_SUPPORTED_FOR_CAMPAIGN_SALES_COUNTRY = 13
        CANNOT_ADD_ADGROUP_OF_TYPE_DSA_TO_CAMPAIGN_WITHOUT_DSA_SETTING = 14


class FieldMaskErrorEnum(object):
    class FieldMaskError(enum.IntEnum):
        """
        Enum describing possible field mask errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          FIELD_MASK_MISSING (int): The field mask must be provided for update operations.
          FIELD_MASK_NOT_ALLOWED (int): The field mask must be empty for create and remove operations.
          FIELD_NOT_FOUND (int): The field mask contained an invalid field.
          FIELD_HAS_SUBFIELDS (int): The field mask updated a field with subfields. Fields with subfields may
          be cleared, but not updated. To fix this, the field mask should select
          all the subfields of the invalid field.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        FIELD_MASK_MISSING = 5
        FIELD_MASK_NOT_ALLOWED = 4
        FIELD_NOT_FOUND = 2
        FIELD_HAS_SUBFIELDS = 3


class StringLengthErrorEnum(object):
    class StringLengthError(enum.IntEnum):
        """
        Enum describing possible string length errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          TOO_SHORT (int): Too short.
          TOO_LONG (int): Too long.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        TOO_SHORT = 2
        TOO_LONG = 3


class AdGroupCriterionErrorEnum(object):
    class AdGroupCriterionError(enum.IntEnum):
        """
        Enum describing possible ad group criterion errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          AD_GROUP_CRITERION_LABEL_DOES_NOT_EXIST (int): No link found between the AdGroupCriterion and the label.
          AD_GROUP_CRITERION_LABEL_ALREADY_EXISTS (int): The label has already been attached to the AdGroupCriterion.
          CANNOT_ADD_LABEL_TO_NEGATIVE_CRITERION (int): Negative AdGroupCriterion cannot have labels.
          TOO_MANY_OPERATIONS (int): Too many operations for a single call.
          CANT_UPDATE_NEGATIVE (int): Negative ad group criteria are not updateable.
          CONCRETE_TYPE_REQUIRED (int): Concrete type of criterion (keyword v.s. placement) is required for ADD
          and SET operations.
          BID_INCOMPATIBLE_WITH_ADGROUP (int): Bid is incompatible with ad group's bidding settings.
          CANNOT_TARGET_AND_EXCLUDE (int): Cannot target and exclude the same criterion at once.
          ILLEGAL_URL (int): The URL of a placement is invalid.
          INVALID_KEYWORD_TEXT (int): Keyword text was invalid.
          INVALID_DESTINATION_URL (int): Destination URL was invalid.
          MISSING_DESTINATION_URL_TAG (int): The destination url must contain at least one tag (e.g. {lpurl})
          KEYWORD_LEVEL_BID_NOT_SUPPORTED_FOR_MANUALCPM (int): Keyword-level cpm bid is not supported
          INVALID_USER_STATUS (int): For example, cannot add a biddable ad group criterion that had been
          removed.
          CANNOT_ADD_CRITERIA_TYPE (int): Criteria type cannot be targeted for the ad group. Either the account is
          restricted to keywords only, the criteria type is incompatible with the
          campaign's bidding strategy, or the criteria type can only be applied to
          campaigns.
          CANNOT_EXCLUDE_CRITERIA_TYPE (int): Criteria type cannot be excluded for the ad group. Refer to the
          documentation for a specific criterion to check if it is excludable.
          CAMPAIGN_TYPE_NOT_COMPATIBLE_WITH_PARTIAL_FAILURE (int): Partial failure is not supported for shopping campaign mutate operations.
          OPERATIONS_FOR_TOO_MANY_SHOPPING_ADGROUPS (int): Operations in the mutate request changes too many shopping ad groups.
          Please split requests for multiple shopping ad groups across multiple
          requests.
          CANNOT_MODIFY_URL_FIELDS_WITH_DUPLICATE_ELEMENTS (int): Not allowed to modify url fields of an ad group criterion if there are
          duplicate elements for that ad group criterion in the request.
          CANNOT_SET_WITHOUT_FINAL_URLS (int): Cannot set url fields without also setting final urls.
          CANNOT_CLEAR_FINAL_URLS_IF_FINAL_MOBILE_URLS_EXIST (int): Cannot clear final urls if final mobile urls exist.
          CANNOT_CLEAR_FINAL_URLS_IF_FINAL_APP_URLS_EXIST (int): Cannot clear final urls if final app urls exist.
          CANNOT_CLEAR_FINAL_URLS_IF_TRACKING_URL_TEMPLATE_EXISTS (int): Cannot clear final urls if tracking url template exists.
          CANNOT_CLEAR_FINAL_URLS_IF_URL_CUSTOM_PARAMETERS_EXIST (int): Cannot clear final urls if url custom parameters exist.
          CANNOT_SET_BOTH_DESTINATION_URL_AND_FINAL_URLS (int): Cannot set both destination url and final urls.
          CANNOT_SET_BOTH_DESTINATION_URL_AND_TRACKING_URL_TEMPLATE (int): Cannot set both destination url and tracking url template.
          FINAL_URLS_NOT_SUPPORTED_FOR_CRITERION_TYPE (int): Final urls are not supported for this criterion type.
          FINAL_MOBILE_URLS_NOT_SUPPORTED_FOR_CRITERION_TYPE (int): Final mobile urls are not supported for this criterion type.
          INVALID_LISTING_GROUP_HIERARCHY (int): Ad group is invalid due to the listing groups it contains.
          LISTING_GROUP_UNIT_CANNOT_HAVE_CHILDREN (int): Listing group unit cannot have children.
          LISTING_GROUP_SUBDIVISION_REQUIRES_OTHERS_CASE (int): Subdivided listing groups must have an \"others\" case.
          LISTING_GROUP_REQUIRES_SAME_DIMENSION_TYPE_AS_SIBLINGS (int): Dimension type of listing group must be the same as that of its siblings.
          LISTING_GROUP_ALREADY_EXISTS (int): Listing group cannot be added to the ad group because it already exists.
          LISTING_GROUP_DOES_NOT_EXIST (int): Listing group referenced in the operation was not found in the ad group.
          LISTING_GROUP_CANNOT_BE_REMOVED (int): Recursive removal failed because listing group subdivision is being
          created or modified in this request.
          INVALID_LISTING_GROUP_TYPE (int): Listing group type is not allowed for specified ad group criterion type.
          LISTING_GROUP_ADD_MAY_ONLY_USE_TEMP_ID (int): Listing group in an ADD operation specifies a non temporary criterion id.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        AD_GROUP_CRITERION_LABEL_DOES_NOT_EXIST = 2
        AD_GROUP_CRITERION_LABEL_ALREADY_EXISTS = 3
        CANNOT_ADD_LABEL_TO_NEGATIVE_CRITERION = 4
        TOO_MANY_OPERATIONS = 5
        CANT_UPDATE_NEGATIVE = 6
        CONCRETE_TYPE_REQUIRED = 7
        BID_INCOMPATIBLE_WITH_ADGROUP = 8
        CANNOT_TARGET_AND_EXCLUDE = 9
        ILLEGAL_URL = 10
        INVALID_KEYWORD_TEXT = 11
        INVALID_DESTINATION_URL = 12
        MISSING_DESTINATION_URL_TAG = 13
        KEYWORD_LEVEL_BID_NOT_SUPPORTED_FOR_MANUALCPM = 14
        INVALID_USER_STATUS = 15
        CANNOT_ADD_CRITERIA_TYPE = 16
        CANNOT_EXCLUDE_CRITERIA_TYPE = 17
        CAMPAIGN_TYPE_NOT_COMPATIBLE_WITH_PARTIAL_FAILURE = 27
        OPERATIONS_FOR_TOO_MANY_SHOPPING_ADGROUPS = 28
        CANNOT_MODIFY_URL_FIELDS_WITH_DUPLICATE_ELEMENTS = 29
        CANNOT_SET_WITHOUT_FINAL_URLS = 30
        CANNOT_CLEAR_FINAL_URLS_IF_FINAL_MOBILE_URLS_EXIST = 31
        CANNOT_CLEAR_FINAL_URLS_IF_FINAL_APP_URLS_EXIST = 32
        CANNOT_CLEAR_FINAL_URLS_IF_TRACKING_URL_TEMPLATE_EXISTS = 33
        CANNOT_CLEAR_FINAL_URLS_IF_URL_CUSTOM_PARAMETERS_EXIST = 34
        CANNOT_SET_BOTH_DESTINATION_URL_AND_FINAL_URLS = 35
        CANNOT_SET_BOTH_DESTINATION_URL_AND_TRACKING_URL_TEMPLATE = 36
        FINAL_URLS_NOT_SUPPORTED_FOR_CRITERION_TYPE = 37
        FINAL_MOBILE_URLS_NOT_SUPPORTED_FOR_CRITERION_TYPE = 38
        INVALID_LISTING_GROUP_HIERARCHY = 39
        LISTING_GROUP_UNIT_CANNOT_HAVE_CHILDREN = 40
        LISTING_GROUP_SUBDIVISION_REQUIRES_OTHERS_CASE = 41
        LISTING_GROUP_REQUIRES_SAME_DIMENSION_TYPE_AS_SIBLINGS = 42
        LISTING_GROUP_ALREADY_EXISTS = 43
        LISTING_GROUP_DOES_NOT_EXIST = 44
        LISTING_GROUP_CANNOT_BE_REMOVED = 45
        INVALID_LISTING_GROUP_TYPE = 46
        LISTING_GROUP_ADD_MAY_ONLY_USE_TEMP_ID = 47


class CampaignSharedSetErrorEnum(object):
    class CampaignSharedSetError(enum.IntEnum):
        """
        Enum describing possible campaign shared set errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          SHARED_SET_ACCESS_DENIED (int): The shared set belongs to another customer and permission isn't granted.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        SHARED_SET_ACCESS_DENIED = 2


class QuotaErrorEnum(object):
    class QuotaError(enum.IntEnum):
        """
        Enum describing possible quota errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          RESOURCE_EXHAUSTED (int): Too many requests.
          ACCESS_PROHIBITED (int): Access is prohibited.
          RESOURCE_TEMPORARILY_EXHAUSTED (int): Too many requests in a short amount of time.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        RESOURCE_EXHAUSTED = 2
        ACCESS_PROHIBITED = 3
        RESOURCE_TEMPORARILY_EXHAUSTED = 4


class FeedAttributeReferenceErrorEnum(object):
    class FeedAttributeReferenceError(enum.IntEnum):
        """
        Enum describing possible feed attribute reference errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CANNOT_REFERENCE_DELETED_FEED (int): A feed referenced by ID has been deleted.
          INVALID_FEED_NAME (int): There is no active feed with the given name.
          INVALID_FEED_ATTRIBUTE_NAME (int): There is no feed attribute in an active feed with the given name.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CANNOT_REFERENCE_DELETED_FEED = 2
        INVALID_FEED_NAME = 3
        INVALID_FEED_ATTRIBUTE_NAME = 4


class MediaFileErrorEnum(object):
    class MediaFileError(enum.IntEnum):
        """
        Enum describing possible media file errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CANNOT_CREATE_STANDARD_ICON (int): Cannot create a standard icon type.
          CANNOT_SELECT_STANDARD_ICON_WITH_OTHER_TYPES (int): May only select Standard Icons alone.
          CANNOT_SPECIFY_MEDIA_FILE_ID_AND_DATA (int): Image contains both a media file ID and data.
          DUPLICATE_MEDIA (int): A media file with given type and reference ID already exists.
          EMPTY_FIELD (int): A required field was not specified or is an empty string.
          RESOURCE_REFERENCED_IN_MULTIPLE_OPS (int): A media file may only be modified once per call.
          FIELD_NOT_SUPPORTED_FOR_MEDIA_SUB_TYPE (int): Field is not supported for the media sub type.
          INVALID_MEDIA_FILE_ID (int): The media file ID is invalid.
          INVALID_MEDIA_SUB_TYPE (int): The media subtype is invalid.
          INVALID_MEDIA_FILE_TYPE (int): The media file type is invalid.
          INVALID_MIME_TYPE (int): The mimetype is invalid.
          INVALID_REFERENCE_ID (int): The media reference ID is invalid.
          INVALID_YOU_TUBE_ID (int): The YouTube video ID is invalid.
          MEDIA_FILE_FAILED_TRANSCODING (int): Media file has failed transcoding
          MEDIA_NOT_TRANSCODED (int): Media file has not been transcoded.
          MEDIA_TYPE_DOES_NOT_MATCH_MEDIA_FILE_TYPE (int): The media type does not match the actual media file's type.
          NO_FIELDS_SPECIFIED (int): None of the fields have been specified.
          NULL_REFERENCE_ID_AND_MEDIA_ID (int): One of reference ID or media file ID must be specified.
          TOO_LONG (int): The string has too many characters.
          UNSUPPORTED_TYPE (int): The specified type is not supported.
          YOU_TUBE_SERVICE_UNAVAILABLE (int): YouTube is unavailable for requesting video data.
          YOU_TUBE_VIDEO_HAS_NON_POSITIVE_DURATION (int): The YouTube video has a non positive duration.
          YOU_TUBE_VIDEO_NOT_FOUND (int): The YouTube video ID is syntactically valid but the video was not found.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CANNOT_CREATE_STANDARD_ICON = 2
        CANNOT_SELECT_STANDARD_ICON_WITH_OTHER_TYPES = 3
        CANNOT_SPECIFY_MEDIA_FILE_ID_AND_DATA = 4
        DUPLICATE_MEDIA = 5
        EMPTY_FIELD = 6
        RESOURCE_REFERENCED_IN_MULTIPLE_OPS = 7
        FIELD_NOT_SUPPORTED_FOR_MEDIA_SUB_TYPE = 8
        INVALID_MEDIA_FILE_ID = 9
        INVALID_MEDIA_SUB_TYPE = 10
        INVALID_MEDIA_FILE_TYPE = 11
        INVALID_MIME_TYPE = 12
        INVALID_REFERENCE_ID = 13
        INVALID_YOU_TUBE_ID = 14
        MEDIA_FILE_FAILED_TRANSCODING = 15
        MEDIA_NOT_TRANSCODED = 16
        MEDIA_TYPE_DOES_NOT_MATCH_MEDIA_FILE_TYPE = 17
        NO_FIELDS_SPECIFIED = 18
        NULL_REFERENCE_ID_AND_MEDIA_ID = 19
        TOO_LONG = 20
        UNSUPPORTED_TYPE = 21
        YOU_TUBE_SERVICE_UNAVAILABLE = 22
        YOU_TUBE_VIDEO_HAS_NON_POSITIVE_DURATION = 23
        YOU_TUBE_VIDEO_NOT_FOUND = 24


class DateErrorEnum(object):
    class DateError(enum.IntEnum):
        """
        Enum describing possible date errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          INVALID_FIELD_VALUES_IN_DATE (int): Given field values do not correspond to a valid date.
          INVALID_FIELD_VALUES_IN_DATE_TIME (int): Given field values do not correspond to a valid date time.
          INVALID_STRING_DATE (int): The string date's format should be yyyymmdd.
          INVALID_STRING_DATE_TIME (int): The string date time's format should be yyyymmdd hhmmss [tz].
          EARLIER_THAN_MINIMUM_DATE (int): Date is before allowed minimum.
          LATER_THAN_MAXIMUM_DATE (int): Date is after allowed maximum.
          DATE_RANGE_MINIMUM_DATE_LATER_THAN_MAXIMUM_DATE (int): Date range bounds are not in order.
          DATE_RANGE_MINIMUM_AND_MAXIMUM_DATES_BOTH_NULL (int): Both dates in range are null.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INVALID_FIELD_VALUES_IN_DATE = 2
        INVALID_FIELD_VALUES_IN_DATE_TIME = 3
        INVALID_STRING_DATE = 4
        INVALID_STRING_DATE_TIME = 6
        EARLIER_THAN_MINIMUM_DATE = 7
        LATER_THAN_MAXIMUM_DATE = 8
        DATE_RANGE_MINIMUM_DATE_LATER_THAN_MAXIMUM_DATE = 9
        DATE_RANGE_MINIMUM_AND_MAXIMUM_DATES_BOTH_NULL = 10


class BiddingErrorEnum(object):
    class BiddingError(enum.IntEnum):
        """
        Enum describing possible bidding errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          BIDDING_STRATEGY_TRANSITION_NOT_ALLOWED (int): Cannot transition to new bidding strategy.
          CANNOT_ATTACH_BIDDING_STRATEGY_TO_CAMPAIGN (int): Cannot attach bidding strategy to campaign.
          INVALID_ANONYMOUS_BIDDING_STRATEGY_TYPE (int): Bidding strategy is not supported or cannot be used as anonymous.
          INVALID_BIDDING_STRATEGY_TYPE (int): The type does not match the named strategy's type.
          INVALID_BID (int): The bid is invalid.
          BIDDING_STRATEGY_NOT_AVAILABLE_FOR_ACCOUNT_TYPE (int): Bidding strategy is not available for the account type.
          CONVERSION_TRACKING_NOT_ENABLED (int): Conversion tracking is not enabled for the campaign for VBB transition.
          NOT_ENOUGH_CONVERSIONS (int): Not enough conversions tracked for VBB transitions.
          CANNOT_CREATE_CAMPAIGN_WITH_BIDDING_STRATEGY (int): Campaign can not be created with given bidding strategy. It can be
          transitioned to the strategy, once eligible.
          CANNOT_TARGET_CONTENT_NETWORK_ONLY_WITH_CAMPAIGN_LEVEL_POP_BIDDING_STRATEGY (int): Cannot target content network only as campaign uses Page One Promoted
          bidding strategy.
          BIDDING_STRATEGY_NOT_SUPPORTED_WITH_AD_SCHEDULE (int): Budget Optimizer and Target Spend bidding strategies are not supported
          for campaigns with AdSchedule targeting.
          PAY_PER_CONVERSION_NOT_AVAILABLE_FOR_CUSTOMER (int): Pay per conversion is not available to all the customer, only few
          whitelisted customers can use this.
          PAY_PER_CONVERSION_NOT_ALLOWED_WITH_TARGET_CPA (int): Pay per conversion is not allowed with Target CPA.
          BIDDING_STRATEGY_NOT_ALLOWED_FOR_SEARCH_ONLY_CAMPAIGNS (int): Cannot set bidding strategy to Manual CPM for search network only
          campaigns.
          BIDDING_STRATEGY_NOT_SUPPORTED_IN_DRAFTS_OR_EXPERIMENTS (int): The bidding strategy is not supported for use in drafts or experiments.
          BIDDING_STRATEGY_TYPE_DOES_NOT_SUPPORT_PRODUCT_TYPE_ADGROUP_CRITERION (int): Bidding strategy type does not support product type ad group criterion.
          BID_TOO_SMALL (int): Bid amount is too small.
          BID_TOO_BIG (int): Bid amount is too big.
          BID_TOO_MANY_FRACTIONAL_DIGITS (int): Bid has too many fractional digit precision.
          INVALID_DOMAIN_NAME (int): Invalid domain name specified.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        BIDDING_STRATEGY_TRANSITION_NOT_ALLOWED = 2
        CANNOT_ATTACH_BIDDING_STRATEGY_TO_CAMPAIGN = 7
        INVALID_ANONYMOUS_BIDDING_STRATEGY_TYPE = 10
        INVALID_BIDDING_STRATEGY_TYPE = 14
        INVALID_BID = 17
        BIDDING_STRATEGY_NOT_AVAILABLE_FOR_ACCOUNT_TYPE = 18
        CONVERSION_TRACKING_NOT_ENABLED = 19
        NOT_ENOUGH_CONVERSIONS = 20
        CANNOT_CREATE_CAMPAIGN_WITH_BIDDING_STRATEGY = 21
        CANNOT_TARGET_CONTENT_NETWORK_ONLY_WITH_CAMPAIGN_LEVEL_POP_BIDDING_STRATEGY = 23
        BIDDING_STRATEGY_NOT_SUPPORTED_WITH_AD_SCHEDULE = 24
        PAY_PER_CONVERSION_NOT_AVAILABLE_FOR_CUSTOMER = 25
        PAY_PER_CONVERSION_NOT_ALLOWED_WITH_TARGET_CPA = 26
        BIDDING_STRATEGY_NOT_ALLOWED_FOR_SEARCH_ONLY_CAMPAIGNS = 27
        BIDDING_STRATEGY_NOT_SUPPORTED_IN_DRAFTS_OR_EXPERIMENTS = 28
        BIDDING_STRATEGY_TYPE_DOES_NOT_SUPPORT_PRODUCT_TYPE_ADGROUP_CRITERION = 29
        BID_TOO_SMALL = 30
        BID_TOO_BIG = 31
        BID_TOO_MANY_FRACTIONAL_DIGITS = 32
        INVALID_DOMAIN_NAME = 33


class StringFormatErrorEnum(object):
    class StringFormatError(enum.IntEnum):
        """
        Enum describing possible string format errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          ILLEGAL_CHARS (int): The input string value contains disallowed characters.
          INVALID_FORMAT (int): The input string value is invalid for the associated field.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ILLEGAL_CHARS = 2
        INVALID_FORMAT = 3


class AdCustomizerErrorEnum(object):
    class AdCustomizerError(enum.IntEnum):
        """
        Enum describing possible ad customizer errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          COUNTDOWN_INVALID_DATE_FORMAT (int): Invalid date argument in countdown function.
          COUNTDOWN_DATE_IN_PAST (int): Countdown end date is in the past.
          COUNTDOWN_INVALID_LOCALE (int): Invalid locale string in countdown function.
          COUNTDOWN_INVALID_START_DAYS_BEFORE (int): Days-before argument to countdown function is not positive.
          UNKNOWN_USER_LIST (int): A user list referenced in an IF function does not exist.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        COUNTDOWN_INVALID_DATE_FORMAT = 2
        COUNTDOWN_DATE_IN_PAST = 3
        COUNTDOWN_INVALID_LOCALE = 4
        COUNTDOWN_INVALID_START_DAYS_BEFORE = 5
        UNKNOWN_USER_LIST = 6


class ChangeStatusErrorEnum(object):
    class ChangeStatusError(enum.IntEnum):
        """
        Enum describing possible change status errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          START_DATE_TOO_OLD (int): The requested start date is too old.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        START_DATE_TOO_OLD = 3


class FieldErrorEnum(object):
    class FieldError(enum.IntEnum):
        """
        Enum describing possible field errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          REQUIRED (int): The required field was not present in the resource.
          IMMUTABLE_FIELD (int): The field attempted to be mutated is immutable.
          INVALID_VALUE (int): The field's value is invalid.
          VALUE_MUST_BE_UNSET (int): The field cannot be set.
          REQUIRED_NONEMPTY_LIST (int): The required repeated field was empty.
          FIELD_CANNOT_BE_CLEARED (int): The field cannot be cleared.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        REQUIRED = 2
        IMMUTABLE_FIELD = 3
        INVALID_VALUE = 4
        VALUE_MUST_BE_UNSET = 5
        REQUIRED_NONEMPTY_LIST = 6
        FIELD_CANNOT_BE_CLEARED = 7


class SettingErrorEnum(object):
    class SettingError(enum.IntEnum):
        """
        Enum describing possible setting errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          SETTING_TYPE_IS_NOT_AVAILABLE (int): The campaign setting is not available for this Google Ads account.
          SETTING_TYPE_IS_NOT_COMPATIBLE_WITH_CAMPAIGN (int): The setting is not compatible with the campaign.
          TARGETING_SETTING_CONTAINS_INVALID_CRITERION_TYPE_GROUP (int): The supplied TargetingSetting contains an invalid CriterionTypeGroup. See
          CriterionTypeGroup documentation for CriterionTypeGroups allowed
          in Campaign or AdGroup TargetingSettings.
          TARGETING_SETTING_DEMOGRAPHIC_CRITERION_TYPE_GROUPS_MUST_BE_SET_TO_TARGET_ALL (int): TargetingSetting must not explicitly
          set any of the Demographic CriterionTypeGroups (AGE_RANGE, GENDER,
          PARENT, INCOME_RANGE) to false (it's okay to not set them at all, in
          which case the system will set them to true automatically).
          TARGETING_SETTING_CANNOT_CHANGE_TARGET_ALL_TO_FALSE_FOR_DEMOGRAPHIC_CRITERION_TYPE_GROUP (int): TargetingSetting cannot change any of
          the Demographic CriterionTypeGroups (AGE_RANGE, GENDER, PARENT,
          INCOME_RANGE) from true to false.
          DYNAMIC_SEARCH_ADS_SETTING_AT_LEAST_ONE_FEED_ID_MUST_BE_PRESENT (int): At least one feed id should be present.
          DYNAMIC_SEARCH_ADS_SETTING_CONTAINS_INVALID_DOMAIN_NAME (int): The supplied DynamicSearchAdsSetting contains an invalid domain name.
          DYNAMIC_SEARCH_ADS_SETTING_CONTAINS_SUBDOMAIN_NAME (int): The supplied DynamicSearchAdsSetting contains a subdomain name.
          DYNAMIC_SEARCH_ADS_SETTING_CONTAINS_INVALID_LANGUAGE_CODE (int): The supplied DynamicSearchAdsSetting contains an invalid language code.
          TARGET_ALL_IS_NOT_ALLOWED_FOR_PLACEMENT_IN_SEARCH_CAMPAIGN (int): TargetingSettings in search campaigns should not have
          CriterionTypeGroup.PLACEMENT set to targetAll.
          UNIVERSAL_APP_CAMPAIGN_SETTING_DUPLICATE_DESCRIPTION (int): Duplicate description in universal app setting description field.
          UNIVERSAL_APP_CAMPAIGN_SETTING_DESCRIPTION_LINE_WIDTH_TOO_LONG (int): Description line width is too long in universal app setting description
          field.
          UNIVERSAL_APP_CAMPAIGN_SETTING_APP_ID_CANNOT_BE_MODIFIED (int): Universal app setting appId field cannot be modified for COMPLETE
          campaigns.
          TOO_MANY_YOUTUBE_MEDIA_IDS_IN_UNIVERSAL_APP_CAMPAIGN (int): YoutubeVideoMediaIds in universal app setting cannot exceed size limit.
          TOO_MANY_IMAGE_MEDIA_IDS_IN_UNIVERSAL_APP_CAMPAIGN (int): ImageMediaIds in universal app setting cannot exceed size limit.
          MEDIA_INCOMPATIBLE_FOR_UNIVERSAL_APP_CAMPAIGN (int): Media is incompatible for universal app campaign.
          TOO_MANY_EXCLAMATION_MARKS (int): Too many exclamation marks in universal app campaign ad text ideas.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        SETTING_TYPE_IS_NOT_AVAILABLE = 3
        SETTING_TYPE_IS_NOT_COMPATIBLE_WITH_CAMPAIGN = 4
        TARGETING_SETTING_CONTAINS_INVALID_CRITERION_TYPE_GROUP = 5
        TARGETING_SETTING_DEMOGRAPHIC_CRITERION_TYPE_GROUPS_MUST_BE_SET_TO_TARGET_ALL = 6
        TARGETING_SETTING_CANNOT_CHANGE_TARGET_ALL_TO_FALSE_FOR_DEMOGRAPHIC_CRITERION_TYPE_GROUP = 7
        DYNAMIC_SEARCH_ADS_SETTING_AT_LEAST_ONE_FEED_ID_MUST_BE_PRESENT = 8
        DYNAMIC_SEARCH_ADS_SETTING_CONTAINS_INVALID_DOMAIN_NAME = 9
        DYNAMIC_SEARCH_ADS_SETTING_CONTAINS_SUBDOMAIN_NAME = 10
        DYNAMIC_SEARCH_ADS_SETTING_CONTAINS_INVALID_LANGUAGE_CODE = 11
        TARGET_ALL_IS_NOT_ALLOWED_FOR_PLACEMENT_IN_SEARCH_CAMPAIGN = 12
        UNIVERSAL_APP_CAMPAIGN_SETTING_DUPLICATE_DESCRIPTION = 13
        UNIVERSAL_APP_CAMPAIGN_SETTING_DESCRIPTION_LINE_WIDTH_TOO_LONG = 14
        UNIVERSAL_APP_CAMPAIGN_SETTING_APP_ID_CANNOT_BE_MODIFIED = 15
        TOO_MANY_YOUTUBE_MEDIA_IDS_IN_UNIVERSAL_APP_CAMPAIGN = 16
        TOO_MANY_IMAGE_MEDIA_IDS_IN_UNIVERSAL_APP_CAMPAIGN = 17
        MEDIA_INCOMPATIBLE_FOR_UNIVERSAL_APP_CAMPAIGN = 18
        TOO_MANY_EXCLAMATION_MARKS = 19


class ConversionActionErrorEnum(object):
    class ConversionActionError(enum.IntEnum):
        """
        Enum describing possible conversion action errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          DUPLICATE_NAME (int): The specified conversion action name already exists.
          DUPLICATE_APP_ID (int): Another conversion action with the specified app id already exists.
          TWO_CONVERSION_ACTIONS_BIDDING_ON_SAME_APP_DOWNLOAD (int): Android first open action conflicts with Google play codeless download
          action tracking the same app.
          BIDDING_ON_SAME_APP_DOWNLOAD_AS_GLOBAL_ACTION (int): Android first open action conflicts with Google play codeless download
          action tracking the same app.
          DATA_DRIVEN_MODEL_WAS_NEVER_GENERATED (int): The attribution model cannot be set to DATA_DRIVEN because a data-driven
          model has never been generated.
          DATA_DRIVEN_MODEL_EXPIRED (int): The attribution model cannot be set to DATA_DRIVEN because the
          data-driven model is expired.
          DATA_DRIVEN_MODEL_STALE (int): The attribution model cannot be set to DATA_DRIVEN because the
          data-driven model is stale.
          DATA_DRIVEN_MODEL_UNKNOWN (int): The attribution model cannot be set to DATA_DRIVEN because the
          data-driven model is unavailable or the conversion action was newly
          added.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DUPLICATE_NAME = 2
        DUPLICATE_APP_ID = 3
        TWO_CONVERSION_ACTIONS_BIDDING_ON_SAME_APP_DOWNLOAD = 4
        BIDDING_ON_SAME_APP_DOWNLOAD_AS_GLOBAL_ACTION = 5
        DATA_DRIVEN_MODEL_WAS_NEVER_GENERATED = 6
        DATA_DRIVEN_MODEL_EXPIRED = 7
        DATA_DRIVEN_MODEL_STALE = 8
        DATA_DRIVEN_MODEL_UNKNOWN = 9


class UrlFieldErrorEnum(object):
    class UrlFieldError(enum.IntEnum):
        """
        Enum describing possible url field errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          INVALID_TRACKING_URL_TEMPLATE (int): The tracking url template is invalid.
          INVALID_TAG_IN_TRACKING_URL_TEMPLATE (int): The tracking url template contains invalid tag.
          MISSING_TRACKING_URL_TEMPLATE_TAG (int): The tracking url template must contain at least one tag (e.g. {lpurl}),
          This applies only to tracking url template associated with website ads or
          product ads.
          MISSING_PROTOCOL_IN_TRACKING_URL_TEMPLATE (int): The tracking url template must start with a valid protocol (or lpurl
          tag).
          INVALID_PROTOCOL_IN_TRACKING_URL_TEMPLATE (int): The tracking url template starts with an invalid protocol.
          MALFORMED_TRACKING_URL_TEMPLATE (int): The tracking url template contains illegal characters.
          MISSING_HOST_IN_TRACKING_URL_TEMPLATE (int): The tracking url template must contain a host name (or lpurl tag).
          INVALID_TLD_IN_TRACKING_URL_TEMPLATE (int): The tracking url template has an invalid or missing top level domain
          extension.
          REDUNDANT_NESTED_TRACKING_URL_TEMPLATE_TAG (int): The tracking url template contains nested occurrences of the same
          conditional tag (i.e. {ifmobile:{ifmobile:x}}).
          INVALID_FINAL_URL (int): The final url is invalid.
          INVALID_TAG_IN_FINAL_URL (int): The final url contains invalid tag.
          REDUNDANT_NESTED_FINAL_URL_TAG (int): The final url contains nested occurrences of the same conditional tag
          (i.e. {ifmobile:{ifmobile:x}}).
          MISSING_PROTOCOL_IN_FINAL_URL (int): The final url must start with a valid protocol.
          INVALID_PROTOCOL_IN_FINAL_URL (int): The final url starts with an invalid protocol.
          MALFORMED_FINAL_URL (int): The final url contains illegal characters.
          MISSING_HOST_IN_FINAL_URL (int): The final url must contain a host name.
          INVALID_TLD_IN_FINAL_URL (int): The tracking url template has an invalid or missing top level domain
          extension.
          INVALID_FINAL_MOBILE_URL (int): The final mobile url is invalid.
          INVALID_TAG_IN_FINAL_MOBILE_URL (int): The final mobile url contains invalid tag.
          REDUNDANT_NESTED_FINAL_MOBILE_URL_TAG (int): The final mobile url contains nested occurrences of the same conditional
          tag (i.e. {ifmobile:{ifmobile:x}}).
          MISSING_PROTOCOL_IN_FINAL_MOBILE_URL (int): The final mobile url must start with a valid protocol.
          INVALID_PROTOCOL_IN_FINAL_MOBILE_URL (int): The final mobile url starts with an invalid protocol.
          MALFORMED_FINAL_MOBILE_URL (int): The final mobile url contains illegal characters.
          MISSING_HOST_IN_FINAL_MOBILE_URL (int): The final mobile url must contain a host name.
          INVALID_TLD_IN_FINAL_MOBILE_URL (int): The tracking url template has an invalid or missing top level domain
          extension.
          INVALID_FINAL_APP_URL (int): The final app url is invalid.
          INVALID_TAG_IN_FINAL_APP_URL (int): The final app url contains invalid tag.
          REDUNDANT_NESTED_FINAL_APP_URL_TAG (int): The final app url contains nested occurrences of the same conditional tag
          (i.e. {ifmobile:{ifmobile:x}}).
          MULTIPLE_APP_URLS_FOR_OSTYPE (int): More than one app url found for the same OS type.
          INVALID_OSTYPE (int): The OS type given for an app url is not valid.
          INVALID_PROTOCOL_FOR_APP_URL (int): The protocol given for an app url is not valid. (E.g. \"android-app://\")
          INVALID_PACKAGE_ID_FOR_APP_URL (int): The package id (app id) given for an app url is not valid.
          URL_CUSTOM_PARAMETERS_COUNT_EXCEEDS_LIMIT (int): The number of url custom parameters for an resource exceeds the maximum
          limit allowed.
          INVALID_CHARACTERS_IN_URL_CUSTOM_PARAMETER_KEY (int): An invalid character appears in the parameter key.
          INVALID_CHARACTERS_IN_URL_CUSTOM_PARAMETER_VALUE (int): An invalid character appears in the parameter value.
          INVALID_TAG_IN_URL_CUSTOM_PARAMETER_VALUE (int): The url custom parameter value fails url tag validation.
          REDUNDANT_NESTED_URL_CUSTOM_PARAMETER_TAG (int): The custom parameter contains nested occurrences of the same conditional
          tag (i.e. {ifmobile:{ifmobile:x}}).
          MISSING_PROTOCOL (int): The protocol (http:// or https://) is missing.
          INVALID_URL (int): The url is invalid.
          DESTINATION_URL_DEPRECATED (int): Destination Url is deprecated.
          INVALID_TAG_IN_URL (int): The url contains invalid tag.
          MISSING_URL_TAG (int): The url must contain at least one tag (e.g. {lpurl}), This applies only
          to urls associated with website ads or product ads.
          DUPLICATE_URL_ID (int): Duplicate url id.
          INVALID_URL_ID (int): Invalid url id.
          FINAL_URL_SUFFIX_MALFORMED (int): The final url suffix cannot begin with '?' or '&' characters and must be
          a valid query string.
          INVALID_TAG_IN_FINAL_URL_SUFFIX (int): The final url suffix cannot contain {lpurl} related or {ignore} tags.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INVALID_TRACKING_URL_TEMPLATE = 2
        INVALID_TAG_IN_TRACKING_URL_TEMPLATE = 3
        MISSING_TRACKING_URL_TEMPLATE_TAG = 4
        MISSING_PROTOCOL_IN_TRACKING_URL_TEMPLATE = 5
        INVALID_PROTOCOL_IN_TRACKING_URL_TEMPLATE = 6
        MALFORMED_TRACKING_URL_TEMPLATE = 7
        MISSING_HOST_IN_TRACKING_URL_TEMPLATE = 8
        INVALID_TLD_IN_TRACKING_URL_TEMPLATE = 9
        REDUNDANT_NESTED_TRACKING_URL_TEMPLATE_TAG = 10
        INVALID_FINAL_URL = 11
        INVALID_TAG_IN_FINAL_URL = 12
        REDUNDANT_NESTED_FINAL_URL_TAG = 13
        MISSING_PROTOCOL_IN_FINAL_URL = 14
        INVALID_PROTOCOL_IN_FINAL_URL = 15
        MALFORMED_FINAL_URL = 16
        MISSING_HOST_IN_FINAL_URL = 17
        INVALID_TLD_IN_FINAL_URL = 18
        INVALID_FINAL_MOBILE_URL = 19
        INVALID_TAG_IN_FINAL_MOBILE_URL = 20
        REDUNDANT_NESTED_FINAL_MOBILE_URL_TAG = 21
        MISSING_PROTOCOL_IN_FINAL_MOBILE_URL = 22
        INVALID_PROTOCOL_IN_FINAL_MOBILE_URL = 23
        MALFORMED_FINAL_MOBILE_URL = 24
        MISSING_HOST_IN_FINAL_MOBILE_URL = 25
        INVALID_TLD_IN_FINAL_MOBILE_URL = 26
        INVALID_FINAL_APP_URL = 27
        INVALID_TAG_IN_FINAL_APP_URL = 28
        REDUNDANT_NESTED_FINAL_APP_URL_TAG = 29
        MULTIPLE_APP_URLS_FOR_OSTYPE = 30
        INVALID_OSTYPE = 31
        INVALID_PROTOCOL_FOR_APP_URL = 32
        INVALID_PACKAGE_ID_FOR_APP_URL = 33
        URL_CUSTOM_PARAMETERS_COUNT_EXCEEDS_LIMIT = 34
        INVALID_CHARACTERS_IN_URL_CUSTOM_PARAMETER_KEY = 39
        INVALID_CHARACTERS_IN_URL_CUSTOM_PARAMETER_VALUE = 40
        INVALID_TAG_IN_URL_CUSTOM_PARAMETER_VALUE = 41
        REDUNDANT_NESTED_URL_CUSTOM_PARAMETER_TAG = 42
        MISSING_PROTOCOL = 43
        INVALID_URL = 44
        DESTINATION_URL_DEPRECATED = 45
        INVALID_TAG_IN_URL = 46
        MISSING_URL_TAG = 47
        DUPLICATE_URL_ID = 48
        INVALID_URL_ID = 49
        FINAL_URL_SUFFIX_MALFORMED = 50
        INVALID_TAG_IN_FINAL_URL_SUFFIX = 51


class PolicyFindingErrorEnum(object):
    class PolicyFindingError(enum.IntEnum):
        """
        Enum describing possible policy finding errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          POLICY_FINDING (int): The resource has been disapproved since the policy summary includes
          policy topics of type PROHIBITED.
          POLICY_TOPIC_NOT_FOUND (int): The given policy topic does not exist.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        POLICY_FINDING = 2
        POLICY_TOPIC_NOT_FOUND = 3


class ResourceAccessDeniedErrorEnum(object):
    class ResourceAccessDeniedError(enum.IntEnum):
        """
        Enum describing possible resource access denied errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          WRITE_ACCESS_DENIED (int): User did not have write access.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        WRITE_ACCESS_DENIED = 3


class ImageErrorEnum(object):
    class ImageError(enum.IntEnum):
        """
        Enum describing possible image errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          INVALID_IMAGE (int): The image is not valid.
          STORAGE_ERROR (int): The image could not be stored.
          BAD_REQUEST (int): There was a problem with the request.
          UNEXPECTED_SIZE (int): The image is not of legal dimensions.
          ANIMATED_NOT_ALLOWED (int): Animated image are not permitted.
          ANIMATION_TOO_LONG (int): Animation is too long.
          SERVER_ERROR (int): There was an error on the server.
          CMYK_JPEG_NOT_ALLOWED (int): Image cannot be in CMYK color format.
          FLASH_NOT_ALLOWED (int): Flash images are not permitted.
          FLASH_WITHOUT_CLICKTAG (int): Flash images must support clickTag.
          FLASH_ERROR_AFTER_FIXING_CLICK_TAG (int): A flash error has occurred after fixing the click tag.
          ANIMATED_VISUAL_EFFECT (int): Unacceptable visual effects.
          FLASH_ERROR (int): There was a problem with the flash image.
          LAYOUT_PROBLEM (int): Incorrect image layout.
          PROBLEM_READING_IMAGE_FILE (int): There was a problem reading the image file.
          ERROR_STORING_IMAGE (int): There was an error storing the image.
          ASPECT_RATIO_NOT_ALLOWED (int): The aspect ratio of the image is not allowed.
          FLASH_HAS_NETWORK_OBJECTS (int): Flash cannot have network objects.
          FLASH_HAS_NETWORK_METHODS (int): Flash cannot have network methods.
          FLASH_HAS_URL (int): Flash cannot have a Url.
          FLASH_HAS_MOUSE_TRACKING (int): Flash cannot use mouse tracking.
          FLASH_HAS_RANDOM_NUM (int): Flash cannot have a random number.
          FLASH_SELF_TARGETS (int): Ad click target cannot be '_self'.
          FLASH_BAD_GETURL_TARGET (int): GetUrl method should only use '_blank'.
          FLASH_VERSION_NOT_SUPPORTED (int): Flash version is not supported.
          FLASH_WITHOUT_HARD_CODED_CLICK_URL (int): Flash movies need to have hard coded click URL or clickTAG
          INVALID_FLASH_FILE (int): Uploaded flash file is corrupted.
          FAILED_TO_FIX_CLICK_TAG_IN_FLASH (int): Uploaded flash file can be parsed, but the click tag can not be fixed
          properly.
          FLASH_ACCESSES_NETWORK_RESOURCES (int): Flash movie accesses network resources
          FLASH_EXTERNAL_JS_CALL (int): Flash movie attempts to call external javascript code
          FLASH_EXTERNAL_FS_CALL (int): Flash movie attempts to call flash system commands
          FILE_TOO_LARGE (int): Image file is too large.
          IMAGE_DATA_TOO_LARGE (int): Image data is too large.
          IMAGE_PROCESSING_ERROR (int): Error while processing the image.
          IMAGE_TOO_SMALL (int): Image is too small.
          INVALID_INPUT (int): Input was invalid.
          PROBLEM_READING_FILE (int): There was a problem reading the image file.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INVALID_IMAGE = 2
        STORAGE_ERROR = 3
        BAD_REQUEST = 4
        UNEXPECTED_SIZE = 5
        ANIMATED_NOT_ALLOWED = 6
        ANIMATION_TOO_LONG = 7
        SERVER_ERROR = 8
        CMYK_JPEG_NOT_ALLOWED = 9
        FLASH_NOT_ALLOWED = 10
        FLASH_WITHOUT_CLICKTAG = 11
        FLASH_ERROR_AFTER_FIXING_CLICK_TAG = 12
        ANIMATED_VISUAL_EFFECT = 13
        FLASH_ERROR = 14
        LAYOUT_PROBLEM = 15
        PROBLEM_READING_IMAGE_FILE = 16
        ERROR_STORING_IMAGE = 17
        ASPECT_RATIO_NOT_ALLOWED = 18
        FLASH_HAS_NETWORK_OBJECTS = 19
        FLASH_HAS_NETWORK_METHODS = 20
        FLASH_HAS_URL = 21
        FLASH_HAS_MOUSE_TRACKING = 22
        FLASH_HAS_RANDOM_NUM = 23
        FLASH_SELF_TARGETS = 24
        FLASH_BAD_GETURL_TARGET = 25
        FLASH_VERSION_NOT_SUPPORTED = 26
        FLASH_WITHOUT_HARD_CODED_CLICK_URL = 27
        INVALID_FLASH_FILE = 28
        FAILED_TO_FIX_CLICK_TAG_IN_FLASH = 29
        FLASH_ACCESSES_NETWORK_RESOURCES = 30
        FLASH_EXTERNAL_JS_CALL = 31
        FLASH_EXTERNAL_FS_CALL = 32
        FILE_TOO_LARGE = 33
        IMAGE_DATA_TOO_LARGE = 34
        IMAGE_PROCESSING_ERROR = 35
        IMAGE_TOO_SMALL = 36
        INVALID_INPUT = 37
        PROBLEM_READING_FILE = 38


class AdSharingErrorEnum(object):
    class AdSharingError(enum.IntEnum):
        """
        Enum describing possible ad sharing errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          AD_GROUP_ALREADY_CONTAINS_AD (int): Error resulting in attempting to add an Ad to an AdGroup that already
          contains the Ad.
          INCOMPATIBLE_AD_UNDER_AD_GROUP (int): Ad is not compatible with the AdGroup it is being shared with.
          CANNOT_SHARE_INACTIVE_AD (int): Cannot add AdGroupAd on inactive Ad.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        AD_GROUP_ALREADY_CONTAINS_AD = 2
        INCOMPATIBLE_AD_UNDER_AD_GROUP = 3
        CANNOT_SHARE_INACTIVE_AD = 4


class DistinctErrorEnum(object):
    class DistinctError(enum.IntEnum):
        """
        Enum describing possible distinct errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          DUPLICATE_ELEMENT (int): Duplicate element.
          DUPLICATE_TYPE (int): Duplicate type.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        DUPLICATE_ELEMENT = 2
        DUPLICATE_TYPE = 3


class InternalErrorEnum(object):
    class InternalError(enum.IntEnum):
        """
        Enum describing possible internal errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          INTERNAL_ERROR (int): Google Ads API encountered unexpected internal error.
          ERROR_CODE_NOT_PUBLISHED (int): The intended error code doesn't exist in any API version. This will be
          fixed by adding a new error code as soon as possible.
          TRANSIENT_ERROR (int): Google Ads API encountered an unexpected transient error. The user
          should retry their request in these cases.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INTERNAL_ERROR = 2
        ERROR_CODE_NOT_PUBLISHED = 3
        TRANSIENT_ERROR = 4


class ResourceCountLimitExceededErrorEnum(object):
    class ResourceCountLimitExceededError(enum.IntEnum):
        """
        Enum describing possible resource count limit exceeded errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          ACCOUNT_LIMIT (int): Indicates that this request would exceed the number of allowed resources
          for the Google Ads account. The exact resource type and limit being
          checked
          can be inferred from accountLimitType.
          CAMPAIGN_LIMIT (int): Indicates that this request would exceed the number of allowed resources
          in a Campaign. The exact resource type and limit being checked can be
          inferred from accountLimitType, and the numeric id of the
          Campaign involved is given by enclosingId.
          ADGROUP_LIMIT (int): Indicates that this request would exceed the number of allowed resources
          in an ad group. The exact resource type and limit being checked can be
          inferred from accountLimitType, and the numeric id of the
          ad group involved is given by enclosingId.
          AD_GROUP_AD_LIMIT (int): Indicates that this request would exceed the number of allowed resources
          in an ad group ad. The exact resource type and limit being checked can
          be inferred from accountLimitType, and the enclosingId
          contains the ad group id followed by the ad id, separated by a single
          comma (,).
          AD_GROUP_CRITERION_LIMIT (int): Indicates that this request would exceed the number of allowed resources
          in an ad group criterion. The exact resource type and limit being checked
          can be inferred from accountLimitType, and the
          enclosingId contains the ad group id followed by the
          criterion id, separated by a single comma (,).
          SHARED_SET_LIMIT (int): Indicates that this request would exceed the number of allowed resources
          in this shared set. The exact resource type and limit being checked can
          be inferred from accountLimitType, and the numeric id of the
          shared set involved is given by enclosingId.
          MATCHING_FUNCTION_LIMIT (int): Exceeds a limit related to a matching function.
          RESPONSE_ROW_LIMIT_EXCEEDED (int): The response for this request would exceed the maximum number of rows
          that can be returned.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ACCOUNT_LIMIT = 2
        CAMPAIGN_LIMIT = 3
        ADGROUP_LIMIT = 4
        AD_GROUP_AD_LIMIT = 5
        AD_GROUP_CRITERION_LIMIT = 6
        SHARED_SET_LIMIT = 7
        MATCHING_FUNCTION_LIMIT = 8
        RESPONSE_ROW_LIMIT_EXCEEDED = 9


class CustomerManagerLinkErrorEnum(object):
    class CustomerManagerLinkError(enum.IntEnum):
        """
        Enum describing possible CustomerManagerLink errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          NO_PENDING_INVITE (int): No pending invitation.
          SAME_CLIENT_MORE_THAN_ONCE_PER_CALL (int): Attempt to operate on the same client more than once in the same call.
          MANAGER_HAS_MAX_NUMBER_OF_LINKED_ACCOUNTS (int): Manager account has the maximum number of linked accounts.
          CANNOT_UNLINK_ACCOUNT_WITHOUT_ACTIVE_USER (int): If no active user on account it cannot be unlinked from its manager.
          CANNOT_REMOVE_LAST_CLIENT_ACCOUNT_OWNER (int): Account should have at least one active owner on it before being
          unlinked.
          CANNOT_CHANGE_ROLE_BY_NON_ACCOUNT_OWNER (int): Only account owners may change their permission role.
          CANNOT_CHANGE_ROLE_FOR_NON_ACTIVE_LINK_ACCOUNT (int): When a client's link to its manager is not active, the link role cannot
          be changed.
          DUPLICATE_CHILD_FOUND (int): Attempt to link a child to a parent that contains or will contain
          duplicate children.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        NO_PENDING_INVITE = 2
        SAME_CLIENT_MORE_THAN_ONCE_PER_CALL = 3
        MANAGER_HAS_MAX_NUMBER_OF_LINKED_ACCOUNTS = 4
        CANNOT_UNLINK_ACCOUNT_WITHOUT_ACTIVE_USER = 5
        CANNOT_REMOVE_LAST_CLIENT_ACCOUNT_OWNER = 6
        CANNOT_CHANGE_ROLE_BY_NON_ACCOUNT_OWNER = 7
        CANNOT_CHANGE_ROLE_FOR_NON_ACTIVE_LINK_ACCOUNT = 8
        DUPLICATE_CHILD_FOUND = 9


class AccountBudgetProposalErrorEnum(object):
    class AccountBudgetProposalError(enum.IntEnum):
        """
        Enum describing possible account budget proposal errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          FIELD_MASK_NOT_ALLOWED (int): The field mask must be empty for create/end/remove proposals.
          IMMUTABLE_FIELD (int): The field cannot be set because of the proposal type.
          REQUIRED_FIELD_MISSING (int): The field is required because of the proposal type.
          CANNOT_CANCEL_APPROVED_PROPOSAL (int): Proposals that have been approved cannot be cancelled.
          CANNOT_REMOVE_UNAPPROVED_BUDGET (int): Budgets that haven't been approved cannot be removed.
          CANNOT_REMOVE_RUNNING_BUDGET (int): Budgets that are currently running cannot be removed.
          CANNOT_END_UNAPPROVED_BUDGET (int): Budgets that haven't been approved cannot be truncated.
          CANNOT_END_INACTIVE_BUDGET (int): Only budgets that are currently running can be truncated.
          BUDGET_NAME_REQUIRED (int): All budgets must have names.
          CANNOT_UPDATE_OLD_BUDGET (int): Expired budgets cannot be edited after a sufficient amount of time has
          passed.
          CANNOT_END_IN_PAST (int): It is not permissible a propose a new budget that ends in the past.
          CANNOT_EXTEND_END_TIME (int): An expired budget cannot be extended to overlap with the running budget.
          PURCHASE_ORDER_NUMBER_REQUIRED (int): A purchase order number is required.
          PENDING_UPDATE_PROPOSAL_EXISTS (int): Budgets that have a pending update cannot be updated.
          MULTIPLE_BUDGETS_NOT_ALLOWED_FOR_UNAPPROVED_BILLING_SETUP (int): Cannot propose more than one budget when the corresponding billing setup
          hasn't been approved.
          CANNOT_UPDATE_START_TIME_FOR_STARTED_BUDGET (int): Cannot update the start time of a budget that has already started.
          SPENDING_LIMIT_LOWER_THAN_ACCRUED_COST_NOT_ALLOWED (int): Cannot update the spending limit of a budget with an amount lower than
          what has already been spent.
          UPDATE_IS_NO_OP (int): Cannot propose a budget update without actually changing any fields.
          END_TIME_MUST_FOLLOW_START_TIME (int): The end time must come after the start time.
          BUDGET_DATE_RANGE_INCOMPATIBLE_WITH_BILLING_SETUP (int): The budget's date range must fall within the date range of its billing
          setup.
          NOT_AUTHORIZED (int): The user is not authorized to mutate budgets for the given billing setup.
          INVALID_BILLING_SETUP (int): Mutates are not allowed for the given billing setup.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        FIELD_MASK_NOT_ALLOWED = 2
        IMMUTABLE_FIELD = 3
        REQUIRED_FIELD_MISSING = 4
        CANNOT_CANCEL_APPROVED_PROPOSAL = 5
        CANNOT_REMOVE_UNAPPROVED_BUDGET = 6
        CANNOT_REMOVE_RUNNING_BUDGET = 7
        CANNOT_END_UNAPPROVED_BUDGET = 8
        CANNOT_END_INACTIVE_BUDGET = 9
        BUDGET_NAME_REQUIRED = 10
        CANNOT_UPDATE_OLD_BUDGET = 11
        CANNOT_END_IN_PAST = 12
        CANNOT_EXTEND_END_TIME = 13
        PURCHASE_ORDER_NUMBER_REQUIRED = 14
        PENDING_UPDATE_PROPOSAL_EXISTS = 15
        MULTIPLE_BUDGETS_NOT_ALLOWED_FOR_UNAPPROVED_BILLING_SETUP = 16
        CANNOT_UPDATE_START_TIME_FOR_STARTED_BUDGET = 17
        SPENDING_LIMIT_LOWER_THAN_ACCRUED_COST_NOT_ALLOWED = 18
        UPDATE_IS_NO_OP = 19
        END_TIME_MUST_FOLLOW_START_TIME = 20
        BUDGET_DATE_RANGE_INCOMPATIBLE_WITH_BILLING_SETUP = 21
        NOT_AUTHORIZED = 22
        INVALID_BILLING_SETUP = 23


class AdErrorEnum(object):
    class AdError(enum.IntEnum):
        """
        Enum describing possible ad errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          AD_CUSTOMIZERS_NOT_SUPPORTED_FOR_AD_TYPE (int): Ad customizers are not supported for ad type.
          APPROXIMATELY_TOO_LONG (int): Estimating character sizes the string is too long.
          APPROXIMATELY_TOO_SHORT (int): Estimating character sizes the string is too short.
          BAD_SNIPPET (int): There is a problem with the snippet.
          CANNOT_MODIFY_AD (int): Cannot modify an ad.
          CANNOT_SET_BUSINESS_NAME_IF_URL_SET (int): business name and url cannot be set at the same time
          CANNOT_SET_FIELD (int): The specified field is incompatible with this ad's type or settings.
          CANNOT_SET_FIELD_WITH_ORIGIN_AD_ID_SET (int): Cannot set field when originAdId is set.
          CANNOT_SET_FIELD_WITH_AD_ID_SET_FOR_SHARING (int): Cannot set field when an existing ad id is set for sharing.
          CANNOT_SET_ALLOW_FLEXIBLE_COLOR_FALSE (int): Cannot set allowFlexibleColor false if no color is provided by user.
          CANNOT_SET_COLOR_CONTROL_WHEN_NATIVE_FORMAT_SETTING (int): When user select native, no color control is allowed because we will
          always respect publisher color for native format serving.
          CANNOT_SET_URL (int): Cannot specify a url for the ad type
          CANNOT_SET_WITHOUT_FINAL_URLS (int): Cannot specify a tracking or mobile url without also setting final urls
          CANNOT_SET_WITH_FINAL_URLS (int): Cannot specify a legacy url and a final url simultaneously
          CANNOT_SET_WITH_TRACKING_URL_TEMPLATE (int): Cannot specify a legacy url and a tracking url template simultaneously in
          a DSA.
          CANNOT_SET_WITH_URL_DATA (int): Cannot specify a urls in UrlData and in template fields simultaneously.
          CANNOT_USE_AD_SUBCLASS_FOR_OPERATOR (int): This operator cannot be used with a subclass of Ad.
          CUSTOMER_NOT_APPROVED_MOBILEADS (int): Customer is not approved for mobile ads.
          CUSTOMER_NOT_APPROVED_THIRDPARTY_ADS (int): Customer is not approved for 3PAS richmedia ads.
          CUSTOMER_NOT_APPROVED_THIRDPARTY_REDIRECT_ADS (int): Customer is not approved for 3PAS redirect richmedia (Ad Exchange) ads.
          CUSTOMER_NOT_ELIGIBLE (int): Not an eligible customer
          CUSTOMER_NOT_ELIGIBLE_FOR_UPDATING_BEACON_URL (int): Customer is not eligible for updating beacon url
          DIMENSION_ALREADY_IN_UNION (int): There already exists an ad with the same dimensions in the union.
          DIMENSION_MUST_BE_SET (int): Ad's dimension must be set before setting union dimension.
          DIMENSION_NOT_IN_UNION (int): Ad's dimension must be included in the union dimensions.
          DISPLAY_URL_CANNOT_BE_SPECIFIED (int): Display Url cannot be specified (applies to Ad Exchange Ads)
          DOMESTIC_PHONE_NUMBER_FORMAT (int): Telephone number contains invalid characters or invalid format. Please
          re-enter your number using digits (0-9), dashes (-), and parentheses
          only.
          EMERGENCY_PHONE_NUMBER (int): Emergency telephone numbers are not allowed. Please enter a valid
          domestic phone number to connect customers to your business.
          EMPTY_FIELD (int): A required field was not specified or is an empty string.
          FEED_ATTRIBUTE_MUST_HAVE_MAPPING_FOR_TYPE_ID (int): A feed attribute referenced in an ad customizer tag is not in the ad
          customizer mapping for the feed.
          FEED_ATTRIBUTE_MAPPING_TYPE_MISMATCH (int): The ad customizer field mapping for the feed attribute does not match the
          expected field type.
          ILLEGAL_AD_CUSTOMIZER_TAG_USE (int): The use of ad customizer tags in the ad text is disallowed. Details in
          trigger.
          ILLEGAL_TAG_USE (int): Tags of the form {PH_x}, where x is a number, are disallowed in ad text.
          INCONSISTENT_DIMENSIONS (int): The dimensions of the ad are specified or derived in multiple ways and
          are not consistent.
          INCONSISTENT_STATUS_IN_TEMPLATE_UNION (int): The status cannot differ among template ads of the same union.
          INCORRECT_LENGTH (int): The length of the string is not valid.
          INELIGIBLE_FOR_UPGRADE (int): The ad is ineligible for upgrade.
          INVALID_AD_ADDRESS_CAMPAIGN_TARGET (int): User cannot create mobile ad for countries targeted in specified
          campaign.
          INVALID_AD_TYPE (int): Invalid Ad type. A specific type of Ad is required.
          INVALID_ATTRIBUTES_FOR_MOBILE_IMAGE (int): Headline, description or phone cannot be present when creating mobile
          image ad.
          INVALID_ATTRIBUTES_FOR_MOBILE_TEXT (int): Image cannot be present when creating mobile text ad.
          INVALID_CALL_TO_ACTION_TEXT (int): Invalid call to action text.
          INVALID_CHARACTER_FOR_URL (int): Invalid character in URL.
          INVALID_COUNTRY_CODE (int): Creative's country code is not valid.
          INVALID_DSA_URL_TAG (int): Invalid use of Dynamic Search Ads tags ({lpurl} etc.)
          INVALID_EXPANDED_DYNAMIC_SEARCH_AD_TAG (int): Invalid use of Expanded Dynamic Search Ads tags ({lpurl} etc.)
          INVALID_INPUT (int): An input error whose real reason was not properly mapped (should not
          happen).
          INVALID_MARKUP_LANGUAGE (int): An invalid markup language was entered.
          INVALID_MOBILE_CARRIER (int): An invalid mobile carrier was entered.
          INVALID_MOBILE_CARRIER_TARGET (int): Specified mobile carriers target a country not targeted by the campaign.
          INVALID_NUMBER_OF_ELEMENTS (int): Wrong number of elements for given element type
          INVALID_PHONE_NUMBER_FORMAT (int): The format of the telephone number is incorrect. Please re-enter the
          number using the correct format.
          INVALID_RICH_MEDIA_CERTIFIED_VENDOR_FORMAT_ID (int): The certified vendor format id is incorrect.
          INVALID_TEMPLATE_DATA (int): The template ad data contains validation errors.
          INVALID_TEMPLATE_ELEMENT_FIELD_TYPE (int): The template field doesn't have have the correct type.
          INVALID_TEMPLATE_ID (int): Invalid template id.
          LINE_TOO_WIDE (int): After substituting replacement strings, the line is too wide.
          MISSING_AD_CUSTOMIZER_MAPPING (int): The feed referenced must have ad customizer mapping to be used in a
          customizer tag.
          MISSING_ADDRESS_COMPONENT (int): Missing address component in template element address field.
          MISSING_ADVERTISEMENT_NAME (int): An ad name must be entered.
          MISSING_BUSINESS_NAME (int): Business name must be entered.
          MISSING_DESCRIPTION1 (int): Description (line 2) must be entered.
          MISSING_DESCRIPTION2 (int): Description (line 3) must be entered.
          MISSING_DESTINATION_URL_TAG (int): The destination url must contain at least one tag (e.g. {lpurl})
          MISSING_LANDING_PAGE_URL_TAG (int): The tracking url template of ExpandedDynamicSearchAd must contain at
          least one tag. (e.g. {lpurl})
          MISSING_DIMENSION (int): A valid dimension must be specified for this ad.
          MISSING_DISPLAY_URL (int): A display URL must be entered.
          MISSING_HEADLINE (int): Headline must be entered.
          MISSING_HEIGHT (int): A height must be entered.
          MISSING_IMAGE (int): An image must be entered.
          MISSING_MARKETING_IMAGE_OR_PRODUCT_VIDEOS (int): Marketing image or product videos are required.
          MISSING_MARKUP_LANGUAGES (int): The markup language in which your site is written must be entered.
          MISSING_MOBILE_CARRIER (int): A mobile carrier must be entered.
          MISSING_PHONE (int): Phone number must be entered.
          MISSING_REQUIRED_TEMPLATE_FIELDS (int): Missing required template fields
          MISSING_TEMPLATE_FIELD_VALUE (int): Missing a required field value
          MISSING_TEXT (int): The ad must have text.
          MISSING_VISIBLE_URL (int): A visible URL must be entered.
          MISSING_WIDTH (int): A width must be entered.
          MULTIPLE_DISTINCT_FEEDS_UNSUPPORTED (int): Only 1 feed can be used as the source of ad customizer substitutions in a
          single ad.
          MUST_USE_TEMP_AD_UNION_ID_ON_ADD (int): TempAdUnionId must be use when adding template ads.
          TOO_LONG (int): The string has too many characters.
          TOO_SHORT (int): The string has too few characters.
          UNION_DIMENSIONS_CANNOT_CHANGE (int): Ad union dimensions cannot change for saved ads.
          UNKNOWN_ADDRESS_COMPONENT (int): Address component is not {country, lat, lng}.
          UNKNOWN_FIELD_NAME (int): Unknown unique field name
          UNKNOWN_UNIQUE_NAME (int): Unknown unique name (template element type specifier)
          UNSUPPORTED_DIMENSIONS (int): Unsupported ad dimension
          URL_INVALID_SCHEME (int): URL starts with an invalid scheme.
          URL_INVALID_TOP_LEVEL_DOMAIN (int): URL ends with an invalid top-level domain name.
          URL_MALFORMED (int): URL contains illegal characters.
          URL_NO_HOST (int): URL must contain a host name.
          URL_NOT_EQUIVALENT (int): URL not equivalent during upgrade.
          URL_HOST_NAME_TOO_LONG (int): URL host name too long to be stored as visible URL (applies to Ad
          Exchange ads)
          URL_NO_SCHEME (int): URL must start with a scheme.
          URL_NO_TOP_LEVEL_DOMAIN (int): URL should end in a valid domain extension, such as .com or .net.
          URL_PATH_NOT_ALLOWED (int): URL must not end with a path.
          URL_PORT_NOT_ALLOWED (int): URL must not specify a port.
          URL_QUERY_NOT_ALLOWED (int): URL must not contain a query.
          URL_SCHEME_BEFORE_DSA_TAG (int): A url scheme is not allowed in front of tag in dest url (e.g.
          http://{lpurl})
          URL_SCHEME_BEFORE_EXPANDED_DYNAMIC_SEARCH_AD_TAG (int): A url scheme is not allowed in front of tag in tracking url template
          (e.g. http://{lpurl})
          USER_DOES_NOT_HAVE_ACCESS_TO_TEMPLATE (int): The user does not have permissions to create a template ad for the given
          template.
          INCONSISTENT_EXPANDABLE_SETTINGS (int): Expandable setting is inconsistent/wrong. For example, an AdX ad is
          invalid if it has a expandable vendor format but no expanding directions
          specified, or expanding directions is specified, but the vendor format is
          not expandable.
          INVALID_FORMAT (int): Format is invalid
          INVALID_FIELD_TEXT (int): The text of this field did not match a pattern of allowed values.
          ELEMENT_NOT_PRESENT (int): Template element is mising
          IMAGE_ERROR (int): Error occurred during image processing
          VALUE_NOT_IN_RANGE (int): The value is not within the valid range
          FIELD_NOT_PRESENT (int): Template element field is not present
          ADDRESS_NOT_COMPLETE (int): Address is incomplete
          ADDRESS_INVALID (int): Invalid address
          VIDEO_RETRIEVAL_ERROR (int): Error retrieving specified video
          AUDIO_ERROR (int): Error processing audio
          INVALID_YOUTUBE_DISPLAY_URL (int): Display URL is incorrect for YouTube PYV ads
          TOO_MANY_PRODUCT_IMAGES (int): Too many product Images in GmailAd
          TOO_MANY_PRODUCT_VIDEOS (int): Too many product Videos in GmailAd
          INCOMPATIBLE_AD_TYPE_AND_DEVICE_PREFERENCE (int): The device preference is not compatible with the ad type
          CALLTRACKING_NOT_SUPPORTED_FOR_COUNTRY (int): Call tracking is not supported for specified country.
          CARRIER_SPECIFIC_SHORT_NUMBER_NOT_ALLOWED (int): Carrier specific short number is not allowed.
          DISALLOWED_NUMBER_TYPE (int): Specified phone number type is disallowed.
          PHONE_NUMBER_NOT_SUPPORTED_FOR_COUNTRY (int): Phone number not supported for country.
          PHONE_NUMBER_NOT_SUPPORTED_WITH_CALLTRACKING_FOR_COUNTRY (int): Phone number not supported with call tracking enabled for country.
          PREMIUM_RATE_NUMBER_NOT_ALLOWED (int): Premium rate phone number is not allowed.
          VANITY_PHONE_NUMBER_NOT_ALLOWED (int): Vanity phone number is not allowed.
          INVALID_CALL_CONVERSION_TYPE_ID (int): Invalid call conversion type id.
          CANNOT_DISABLE_CALL_CONVERSION_AND_SET_CONVERSION_TYPE_ID (int): Cannot disable call conversion and set conversion type id.
          CANNOT_SET_PATH2_WITHOUT_PATH1 (int): Cannot set path2 without path1.
          MISSING_DYNAMIC_SEARCH_ADS_SETTING_DOMAIN_NAME (int): Missing domain name in campaign setting when adding expanded dynamic
          search ad.
          INCOMPATIBLE_WITH_RESTRICTION_TYPE (int): The associated ad is not compatible with restriction type.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        AD_CUSTOMIZERS_NOT_SUPPORTED_FOR_AD_TYPE = 2
        APPROXIMATELY_TOO_LONG = 3
        APPROXIMATELY_TOO_SHORT = 4
        BAD_SNIPPET = 5
        CANNOT_MODIFY_AD = 6
        CANNOT_SET_BUSINESS_NAME_IF_URL_SET = 7
        CANNOT_SET_FIELD = 8
        CANNOT_SET_FIELD_WITH_ORIGIN_AD_ID_SET = 9
        CANNOT_SET_FIELD_WITH_AD_ID_SET_FOR_SHARING = 10
        CANNOT_SET_ALLOW_FLEXIBLE_COLOR_FALSE = 11
        CANNOT_SET_COLOR_CONTROL_WHEN_NATIVE_FORMAT_SETTING = 12
        CANNOT_SET_URL = 13
        CANNOT_SET_WITHOUT_FINAL_URLS = 14
        CANNOT_SET_WITH_FINAL_URLS = 15
        CANNOT_SET_WITH_TRACKING_URL_TEMPLATE = 16
        CANNOT_SET_WITH_URL_DATA = 17
        CANNOT_USE_AD_SUBCLASS_FOR_OPERATOR = 18
        CUSTOMER_NOT_APPROVED_MOBILEADS = 19
        CUSTOMER_NOT_APPROVED_THIRDPARTY_ADS = 20
        CUSTOMER_NOT_APPROVED_THIRDPARTY_REDIRECT_ADS = 21
        CUSTOMER_NOT_ELIGIBLE = 22
        CUSTOMER_NOT_ELIGIBLE_FOR_UPDATING_BEACON_URL = 23
        DIMENSION_ALREADY_IN_UNION = 24
        DIMENSION_MUST_BE_SET = 25
        DIMENSION_NOT_IN_UNION = 26
        DISPLAY_URL_CANNOT_BE_SPECIFIED = 27
        DOMESTIC_PHONE_NUMBER_FORMAT = 28
        EMERGENCY_PHONE_NUMBER = 29
        EMPTY_FIELD = 30
        FEED_ATTRIBUTE_MUST_HAVE_MAPPING_FOR_TYPE_ID = 31
        FEED_ATTRIBUTE_MAPPING_TYPE_MISMATCH = 32
        ILLEGAL_AD_CUSTOMIZER_TAG_USE = 33
        ILLEGAL_TAG_USE = 34
        INCONSISTENT_DIMENSIONS = 35
        INCONSISTENT_STATUS_IN_TEMPLATE_UNION = 36
        INCORRECT_LENGTH = 37
        INELIGIBLE_FOR_UPGRADE = 38
        INVALID_AD_ADDRESS_CAMPAIGN_TARGET = 39
        INVALID_AD_TYPE = 40
        INVALID_ATTRIBUTES_FOR_MOBILE_IMAGE = 41
        INVALID_ATTRIBUTES_FOR_MOBILE_TEXT = 42
        INVALID_CALL_TO_ACTION_TEXT = 43
        INVALID_CHARACTER_FOR_URL = 44
        INVALID_COUNTRY_CODE = 45
        INVALID_DSA_URL_TAG = 46
        INVALID_EXPANDED_DYNAMIC_SEARCH_AD_TAG = 47
        INVALID_INPUT = 48
        INVALID_MARKUP_LANGUAGE = 49
        INVALID_MOBILE_CARRIER = 50
        INVALID_MOBILE_CARRIER_TARGET = 51
        INVALID_NUMBER_OF_ELEMENTS = 52
        INVALID_PHONE_NUMBER_FORMAT = 53
        INVALID_RICH_MEDIA_CERTIFIED_VENDOR_FORMAT_ID = 54
        INVALID_TEMPLATE_DATA = 55
        INVALID_TEMPLATE_ELEMENT_FIELD_TYPE = 56
        INVALID_TEMPLATE_ID = 57
        LINE_TOO_WIDE = 58
        MISSING_AD_CUSTOMIZER_MAPPING = 59
        MISSING_ADDRESS_COMPONENT = 60
        MISSING_ADVERTISEMENT_NAME = 61
        MISSING_BUSINESS_NAME = 62
        MISSING_DESCRIPTION1 = 63
        MISSING_DESCRIPTION2 = 64
        MISSING_DESTINATION_URL_TAG = 65
        MISSING_LANDING_PAGE_URL_TAG = 66
        MISSING_DIMENSION = 67
        MISSING_DISPLAY_URL = 68
        MISSING_HEADLINE = 69
        MISSING_HEIGHT = 70
        MISSING_IMAGE = 71
        MISSING_MARKETING_IMAGE_OR_PRODUCT_VIDEOS = 72
        MISSING_MARKUP_LANGUAGES = 73
        MISSING_MOBILE_CARRIER = 74
        MISSING_PHONE = 75
        MISSING_REQUIRED_TEMPLATE_FIELDS = 76
        MISSING_TEMPLATE_FIELD_VALUE = 77
        MISSING_TEXT = 78
        MISSING_VISIBLE_URL = 79
        MISSING_WIDTH = 80
        MULTIPLE_DISTINCT_FEEDS_UNSUPPORTED = 81
        MUST_USE_TEMP_AD_UNION_ID_ON_ADD = 82
        TOO_LONG = 83
        TOO_SHORT = 84
        UNION_DIMENSIONS_CANNOT_CHANGE = 85
        UNKNOWN_ADDRESS_COMPONENT = 86
        UNKNOWN_FIELD_NAME = 87
        UNKNOWN_UNIQUE_NAME = 88
        UNSUPPORTED_DIMENSIONS = 89
        URL_INVALID_SCHEME = 90
        URL_INVALID_TOP_LEVEL_DOMAIN = 91
        URL_MALFORMED = 92
        URL_NO_HOST = 93
        URL_NOT_EQUIVALENT = 94
        URL_HOST_NAME_TOO_LONG = 95
        URL_NO_SCHEME = 96
        URL_NO_TOP_LEVEL_DOMAIN = 97
        URL_PATH_NOT_ALLOWED = 98
        URL_PORT_NOT_ALLOWED = 99
        URL_QUERY_NOT_ALLOWED = 100
        URL_SCHEME_BEFORE_DSA_TAG = 101
        URL_SCHEME_BEFORE_EXPANDED_DYNAMIC_SEARCH_AD_TAG = 102
        USER_DOES_NOT_HAVE_ACCESS_TO_TEMPLATE = 103
        INCONSISTENT_EXPANDABLE_SETTINGS = 104
        INVALID_FORMAT = 105
        INVALID_FIELD_TEXT = 106
        ELEMENT_NOT_PRESENT = 107
        IMAGE_ERROR = 108
        VALUE_NOT_IN_RANGE = 109
        FIELD_NOT_PRESENT = 110
        ADDRESS_NOT_COMPLETE = 111
        ADDRESS_INVALID = 112
        VIDEO_RETRIEVAL_ERROR = 113
        AUDIO_ERROR = 114
        INVALID_YOUTUBE_DISPLAY_URL = 115
        TOO_MANY_PRODUCT_IMAGES = 116
        TOO_MANY_PRODUCT_VIDEOS = 117
        INCOMPATIBLE_AD_TYPE_AND_DEVICE_PREFERENCE = 118
        CALLTRACKING_NOT_SUPPORTED_FOR_COUNTRY = 119
        CARRIER_SPECIFIC_SHORT_NUMBER_NOT_ALLOWED = 120
        DISALLOWED_NUMBER_TYPE = 121
        PHONE_NUMBER_NOT_SUPPORTED_FOR_COUNTRY = 122
        PHONE_NUMBER_NOT_SUPPORTED_WITH_CALLTRACKING_FOR_COUNTRY = 123
        PREMIUM_RATE_NUMBER_NOT_ALLOWED = 124
        VANITY_PHONE_NUMBER_NOT_ALLOWED = 125
        INVALID_CALL_CONVERSION_TYPE_ID = 126
        CANNOT_DISABLE_CALL_CONVERSION_AND_SET_CONVERSION_TYPE_ID = 127
        CANNOT_SET_PATH2_WITHOUT_PATH1 = 128
        MISSING_DYNAMIC_SEARCH_ADS_SETTING_DOMAIN_NAME = 129
        INCOMPATIBLE_WITH_RESTRICTION_TYPE = 130


class AdGroupAdErrorEnum(object):
    class AdGroupAdError(enum.IntEnum):
        """
        Enum describing possible ad group ad errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          AD_GROUP_AD_LABEL_DOES_NOT_EXIST (int): No link found between the adgroup ad and the label.
          AD_GROUP_AD_LABEL_ALREADY_EXISTS (int): The label has already been attached to the adgroup ad.
          AD_NOT_UNDER_ADGROUP (int): The specified ad was not found in the adgroup
          CANNOT_OPERATE_ON_REMOVED_ADGROUPAD (int): Removed ads may not be modified
          CANNOT_CREATE_DEPRECATED_ADS (int): An ad of this type is deprecated and cannot be created. Only deletions
          are permitted.
          CANNOT_CREATE_TEXT_ADS (int): Text ads are deprecated and cannot be created. Use expanded text ads
          instead.
          EMPTY_FIELD (int): A required field was not specified or is an empty string.
          RESOURCE_REFERENCED_IN_MULTIPLE_OPS (int): An ad may only be modified once per call
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        AD_GROUP_AD_LABEL_DOES_NOT_EXIST = 2
        AD_GROUP_AD_LABEL_ALREADY_EXISTS = 3
        AD_NOT_UNDER_ADGROUP = 4
        CANNOT_OPERATE_ON_REMOVED_ADGROUPAD = 5
        CANNOT_CREATE_DEPRECATED_ADS = 6
        CANNOT_CREATE_TEXT_ADS = 7
        EMPTY_FIELD = 8
        RESOURCE_REFERENCED_IN_MULTIPLE_OPS = 9


class AuthenticationErrorEnum(object):
    class AuthenticationError(enum.IntEnum):
        """
        Enum describing possible authentication errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          AUTHENTICATION_ERROR (int): Authentication of the request failed.
          CLIENT_CUSTOMER_ID_INVALID (int): Client customer Id is not a number.
          CUSTOMER_NOT_FOUND (int): No customer found for the provided customer id.
          GOOGLE_ACCOUNT_DELETED (int): Client's Google Account is deleted.
          GOOGLE_ACCOUNT_COOKIE_INVALID (int): Google account login token in the cookie is invalid.
          FAILED_TO_AUTHENTICATE_GOOGLE_ACCOUNT (int): A problem occurred during Google account authentication.
          GOOGLE_ACCOUNT_USER_AND_ADS_USER_MISMATCH (int): The user in the google account login token does not match the UserId in
          the cookie.
          LOGIN_COOKIE_REQUIRED (int): Login cookie is required for authentication.
          NOT_ADS_USER (int): User in the cookie is not a valid Ads user.
          OAUTH_TOKEN_INVALID (int): Oauth token in the header is not valid.
          OAUTH_TOKEN_EXPIRED (int): Oauth token in the header has expired.
          OAUTH_TOKEN_DISABLED (int): Oauth token in the header has been disabled.
          OAUTH_TOKEN_REVOKED (int): Oauth token in the header has been revoked.
          OAUTH_TOKEN_HEADER_INVALID (int): Oauth token HTTP header is malformed.
          LOGIN_COOKIE_INVALID (int): Login cookie is not valid.
          FAILED_TO_RETRIEVE_LOGIN_COOKIE (int): Failed to decrypt the login cookie.
          USER_ID_INVALID (int): User Id in the header is not a valid id.
          TWO_STEP_VERIFICATION_NOT_ENROLLED (int): An account administrator changed this account's authentication settings.
          To access this Google Ads account, enable 2-Step Verification in your
          Google account at https://www.google.com/landing/2step.
          ADVANCED_PROTECTION_NOT_ENROLLED (int): An account administrator changed this account's authentication settings.
          To access this Google Ads account, enable Advanced Protection in your
          Google account at https://landing.google.com/advancedprotection.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        AUTHENTICATION_ERROR = 2
        CLIENT_CUSTOMER_ID_INVALID = 5
        CUSTOMER_NOT_FOUND = 8
        GOOGLE_ACCOUNT_DELETED = 9
        GOOGLE_ACCOUNT_COOKIE_INVALID = 10
        FAILED_TO_AUTHENTICATE_GOOGLE_ACCOUNT = 11
        GOOGLE_ACCOUNT_USER_AND_ADS_USER_MISMATCH = 12
        LOGIN_COOKIE_REQUIRED = 13
        NOT_ADS_USER = 14
        OAUTH_TOKEN_INVALID = 15
        OAUTH_TOKEN_EXPIRED = 16
        OAUTH_TOKEN_DISABLED = 17
        OAUTH_TOKEN_REVOKED = 18
        OAUTH_TOKEN_HEADER_INVALID = 19
        LOGIN_COOKIE_INVALID = 20
        FAILED_TO_RETRIEVE_LOGIN_COOKIE = 21
        USER_ID_INVALID = 22
        TWO_STEP_VERIFICATION_NOT_ENROLLED = 23
        ADVANCED_PROTECTION_NOT_ENROLLED = 24


class AuthorizationErrorEnum(object):
    class AuthorizationError(enum.IntEnum):
        """
        Enum describing possible authorization errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          USER_PERMISSION_DENIED (int): User doesn't have permission to access customer.
          DEVELOPER_TOKEN_NOT_WHITELISTED (int): The developer token is not whitelisted.
          DEVELOPER_TOKEN_PROHIBITED (int): The developer token is not allowed with the project sent in the request.
          PROJECT_DISABLED (int): The Google Cloud project sent in the request does not have permission to
          access the api.
          AUTHORIZATION_ERROR (int): Authorization of the client failed.
          ACTION_NOT_PERMITTED (int): The user does not have permission to perform this action
          (e.g., ADD, UPDATE, REMOVE) on the resource or call a method.
          INCOMPLETE_SIGNUP (int): Signup not complete.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        USER_PERMISSION_DENIED = 2
        DEVELOPER_TOKEN_NOT_WHITELISTED = 3
        DEVELOPER_TOKEN_PROHIBITED = 4
        PROJECT_DISABLED = 5
        AUTHORIZATION_ERROR = 6
        ACTION_NOT_PERMITTED = 7
        INCOMPLETE_SIGNUP = 8


class BillingSetupErrorEnum(object):
    class BillingSetupError(enum.IntEnum):
        """
        Enum describing possible billing setup errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CANNOT_USE_EXISTING_AND_NEW_ACCOUNT (int): Cannot use both an existing Payments account and a new Payments account
          when setting up billing.
          CANNOT_REMOVE_STARTED_BILLING_SETUP (int): Cannot cancel an APPROVED billing setup whose start time has passed.
          CANNOT_CHANGE_BILLING_TO_SAME_PAYMENTS_ACCOUNT (int): Cannot perform a Change of Bill-To (CBT) to the same Payments account.
          BILLING_SETUP_NOT_PERMITTED_FOR_CUSTOMER_STATUS (int): Billing Setups can only be used by customers with ENABLED or DRAFT
          status.
          INVALID_PAYMENTS_ACCOUNT (int): Billing Setups must either include a correctly formatted existing
          Payments account id, or a non-empty new Payments account name.
          BILLING_SETUP_NOT_PERMITTED_FOR_CUSTOMER_CATEGORY (int): Only billable and third party customers can create billing setups.
          INVALID_START_TIME_TYPE (int): Billing Setup creations can only use NOW for start time type.
          THIRD_PARTY_ALREADY_HAS_BILLING (int): Billing Setups can only be created for a third party customer if they do
          not already have a setup.
          BILLING_SETUP_IN_PROGRESS (int): Billing Setups cannot be created if there is already a pending billing in
          progress, ie. a billing known to Payments.
          NO_SIGNUP_PERMISSION (int): Billing Setups can only be created by customers who have permission to
          setup billings. Users can contact a representative for help setting up
          permissions.
          CHANGE_OF_BILL_TO_IN_PROGRESS (int): Billing Setups cannot be created if there is already a future-approved
          billing.
          PAYMENTS_PROFILE_NOT_FOUND (int): Billing Setup creation failed because Payments could not find the
          requested Payments profile.
          PAYMENTS_ACCOUNT_NOT_FOUND (int): Billing Setup creation failed because Payments could not find the
          requested Payments account.
          PAYMENTS_PROFILE_INELIGIBLE (int): Billing Setup creation failed because Payments considers requested
          Payments profile ineligible.
          PAYMENTS_ACCOUNT_INELIGIBLE (int): Billing Setup creation failed because Payments considers requested
          Payments account ineligible.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CANNOT_USE_EXISTING_AND_NEW_ACCOUNT = 2
        CANNOT_REMOVE_STARTED_BILLING_SETUP = 3
        CANNOT_CHANGE_BILLING_TO_SAME_PAYMENTS_ACCOUNT = 4
        BILLING_SETUP_NOT_PERMITTED_FOR_CUSTOMER_STATUS = 5
        INVALID_PAYMENTS_ACCOUNT = 6
        BILLING_SETUP_NOT_PERMITTED_FOR_CUSTOMER_CATEGORY = 7
        INVALID_START_TIME_TYPE = 8
        THIRD_PARTY_ALREADY_HAS_BILLING = 9
        BILLING_SETUP_IN_PROGRESS = 10
        NO_SIGNUP_PERMISSION = 11
        CHANGE_OF_BILL_TO_IN_PROGRESS = 12
        PAYMENTS_PROFILE_NOT_FOUND = 13
        PAYMENTS_ACCOUNT_NOT_FOUND = 14
        PAYMENTS_PROFILE_INELIGIBLE = 15
        PAYMENTS_ACCOUNT_INELIGIBLE = 16


class CampaignBudgetErrorEnum(object):
    class CampaignBudgetError(enum.IntEnum):
        """
        Enum describing possible campaign budget errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CAMPAIGN_BUDGET_CANNOT_BE_SHARED (int): The campaign budget cannot be shared.
          CAMPAIGN_BUDGET_REMOVED (int): The requested campaign budget no longer exists.
          CAMPAIGN_BUDGET_IN_USE (int): The campaign budget is associated with at least one campaign, and so the
          campaign budget cannot be removed.
          CAMPAIGN_BUDGET_PERIOD_NOT_AVAILABLE (int): Customer is not whitelisted for this campaign budget period.
          CANNOT_MODIFY_FIELD_OF_IMPLICITLY_SHARED_CAMPAIGN_BUDGET (int): This field is not mutable on implicitly shared campaign budgets
          CANNOT_UPDATE_CAMPAIGN_BUDGET_TO_IMPLICITLY_SHARED (int): Cannot change explicitly shared campaign budgets back to implicitly
          shared ones.
          CANNOT_UPDATE_CAMPAIGN_BUDGET_TO_EXPLICITLY_SHARED_WITHOUT_NAME (int): An implicit campaign budget without a name cannot be changed to
          explicitly shared campaign budget.
          CANNOT_UPDATE_CAMPAIGN_BUDGET_TO_EXPLICITLY_SHARED (int): Cannot change an implicitly shared campaign budget to an explicitly
          shared one.
          CANNOT_USE_IMPLICITLY_SHARED_CAMPAIGN_BUDGET_WITH_MULTIPLE_CAMPAIGNS (int): Only explicitly shared campaign budgets can be used with multiple
          campaigns.
          DUPLICATE_NAME (int): A campaign budget with this name already exists.
          MONEY_AMOUNT_IN_WRONG_CURRENCY (int): A money amount was not in the expected currency.
          MONEY_AMOUNT_LESS_THAN_CURRENCY_MINIMUM_CPC (int): A money amount was less than the minimum CPC for currency.
          MONEY_AMOUNT_TOO_LARGE (int): A money amount was greater than the maximum allowed.
          NEGATIVE_MONEY_AMOUNT (int): A money amount was negative.
          NON_MULTIPLE_OF_MINIMUM_CURRENCY_UNIT (int): A money amount was not a multiple of a minimum unit.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CAMPAIGN_BUDGET_CANNOT_BE_SHARED = 17
        CAMPAIGN_BUDGET_REMOVED = 2
        CAMPAIGN_BUDGET_IN_USE = 3
        CAMPAIGN_BUDGET_PERIOD_NOT_AVAILABLE = 4
        CANNOT_MODIFY_FIELD_OF_IMPLICITLY_SHARED_CAMPAIGN_BUDGET = 6
        CANNOT_UPDATE_CAMPAIGN_BUDGET_TO_IMPLICITLY_SHARED = 7
        CANNOT_UPDATE_CAMPAIGN_BUDGET_TO_EXPLICITLY_SHARED_WITHOUT_NAME = 8
        CANNOT_UPDATE_CAMPAIGN_BUDGET_TO_EXPLICITLY_SHARED = 9
        CANNOT_USE_IMPLICITLY_SHARED_CAMPAIGN_BUDGET_WITH_MULTIPLE_CAMPAIGNS = 10
        DUPLICATE_NAME = 11
        MONEY_AMOUNT_IN_WRONG_CURRENCY = 12
        MONEY_AMOUNT_LESS_THAN_CURRENCY_MINIMUM_CPC = 13
        MONEY_AMOUNT_TOO_LARGE = 14
        NEGATIVE_MONEY_AMOUNT = 15
        NON_MULTIPLE_OF_MINIMUM_CURRENCY_UNIT = 16


class CampaignCriterionErrorEnum(object):
    class CampaignCriterionError(enum.IntEnum):
        """
        Enum describing possible campaign criterion errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CONCRETE_TYPE_REQUIRED (int): Concrete type of criterion (keyword v.s. placement) is required for
          CREATE and UPDATE operations.
          INVALID_PLACEMENT_URL (int): Invalid placement URL.
          CANNOT_EXCLUDE_CRITERIA_TYPE (int): Criteria type can not be excluded for the campaign by the customer. like
          AOL account type cannot target site type criteria
          CANNOT_SET_STATUS_FOR_CRITERIA_TYPE (int): Cannot set the campaign criterion status for this criteria type.
          CANNOT_SET_STATUS_FOR_EXCLUDED_CRITERIA (int): Cannot set the campaign criterion status for an excluded criteria.
          CANNOT_TARGET_AND_EXCLUDE (int): Cannot target and exclude the same criterion.
          TOO_MANY_OPERATIONS (int): The mutate contained too many operations.
          OPERATOR_NOT_SUPPORTED_FOR_CRITERION_TYPE (int): This operator cannot be applied to a criterion of this type.
          SHOPPING_CAMPAIGN_SALES_COUNTRY_NOT_SUPPORTED_FOR_SALES_CHANNEL (int): The Shopping campaign sales country is not supported for
          ProductSalesChannel targeting.
          CANNOT_ADD_EXISTING_FIELD (int): The existing field can't be updated with CREATE operation. It can be
          updated with UPDATE operation only.
          CANNOT_UPDATE_NEGATIVE_CRITERION (int): Negative criteria are immutable, so updates are not allowed.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CONCRETE_TYPE_REQUIRED = 2
        INVALID_PLACEMENT_URL = 3
        CANNOT_EXCLUDE_CRITERIA_TYPE = 4
        CANNOT_SET_STATUS_FOR_CRITERIA_TYPE = 5
        CANNOT_SET_STATUS_FOR_EXCLUDED_CRITERIA = 6
        CANNOT_TARGET_AND_EXCLUDE = 7
        TOO_MANY_OPERATIONS = 8
        OPERATOR_NOT_SUPPORTED_FOR_CRITERION_TYPE = 9
        SHOPPING_CAMPAIGN_SALES_COUNTRY_NOT_SUPPORTED_FOR_SALES_CHANNEL = 10
        CANNOT_ADD_EXISTING_FIELD = 11
        CANNOT_UPDATE_NEGATIVE_CRITERION = 12


class CampaignErrorEnum(object):
    class CampaignError(enum.IntEnum):
        """
        Enum describing possible campaign errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CANNOT_TARGET_CONTENT_NETWORK (int): Cannot target content network.
          CANNOT_TARGET_SEARCH_NETWORK (int): Cannot target search network.
          CANNOT_TARGET_SEARCH_NETWORK_WITHOUT_GOOGLE_SEARCH (int): Cannot cover search network without google search network.
          CANNOT_TARGET_GOOGLE_SEARCH_FOR_CPM_CAMPAIGN (int): Cannot target Google Search network for a CPM campaign.
          CAMPAIGN_MUST_TARGET_AT_LEAST_ONE_NETWORK (int): Must target at least one network.
          CANNOT_TARGET_PARTNER_SEARCH_NETWORK (int): Only some Google partners are allowed to target partner search network.
          CANNOT_TARGET_CONTENT_NETWORK_ONLY_WITH_CRITERIA_LEVEL_BIDDING_STRATEGY (int): Cannot target content network only as campaign has criteria-level bidding
          strategy.
          CAMPAIGN_DURATION_MUST_CONTAIN_ALL_RUNNABLE_TRIALS (int): Cannot modify the start or end date such that the campaign duration would
          not contain the durations of all runnable trials.
          CANNOT_MODIFY_FOR_TRIAL_CAMPAIGN (int): Cannot modify dates, budget or campaign name of a trial campaign.
          DUPLICATE_CAMPAIGN_NAME (int): Trying to modify the name of an active or paused campaign, where the name
          is already assigned to another active or paused campaign.
          INCOMPATIBLE_CAMPAIGN_FIELD (int): Two fields are in conflicting modes.
          INVALID_CAMPAIGN_NAME (int): Campaign name cannot be used.
          INVALID_AD_SERVING_OPTIMIZATION_STATUS (int): Given status is invalid.
          INVALID_TRACKING_URL (int): Error in the campaign level tracking url.
          CANNOT_SET_BOTH_TRACKING_URL_TEMPLATE_AND_TRACKING_SETTING (int): Cannot set both tracking url template and tracking setting. An user has
          to clear legacy tracking setting in order to add tracking url template.
          MAX_IMPRESSIONS_NOT_IN_RANGE (int): The maximum number of impressions for Frequency Cap should be an integer
          greater than 0.
          TIME_UNIT_NOT_SUPPORTED (int): Only the Day, Week and Month time units are supported.
          INVALID_OPERATION_IF_SERVING_STATUS_HAS_ENDED (int): Operation not allowed on a campaign whose serving status has ended
          BUDGET_CANNOT_BE_SHARED (int): This budget is exclusively linked to a Campaign that is using experiments
          so it cannot be shared.
          CAMPAIGN_CANNOT_USE_SHARED_BUDGET (int): Campaigns using experiments cannot use a shared budget.
          CANNOT_CHANGE_BUDGET_ON_CAMPAIGN_WITH_TRIALS (int): A different budget cannot be assigned to a campaign when there are
          running or scheduled trials.
          CAMPAIGN_LABEL_DOES_NOT_EXIST (int): No link found between the campaign and the label.
          CAMPAIGN_LABEL_ALREADY_EXISTS (int): The label has already been attached to the campaign.
          MISSING_SHOPPING_SETTING (int): A ShoppingSetting was not found when creating a shopping campaign.
          INVALID_SHOPPING_SALES_COUNTRY (int): The country in shopping setting is not an allowed country.
          MISSING_UNIVERSAL_APP_CAMPAIGN_SETTING (int): A Campaign with channel sub type UNIVERSAL_APP_CAMPAIGN must have a
          UniversalAppCampaignSetting specified.
          ADVERTISING_CHANNEL_TYPE_NOT_AVAILABLE_FOR_ACCOUNT_TYPE (int): The requested channel type is not available according to the customer's
          account setting.
          INVALID_ADVERTISING_CHANNEL_SUB_TYPE (int): The AdvertisingChannelSubType is not a valid subtype of the primary
          channel type.
          AT_LEAST_ONE_CONVERSION_MUST_BE_SELECTED (int): At least one conversion must be selected.
          CANNOT_SET_AD_ROTATION_MODE (int): Setting ad rotation mode for a campaign is not allowed. Ad rotation mode
          at campaign is deprecated.
          CANNOT_MODIFY_START_DATE_IF_ALREADY_STARTED (int): Trying to change start date on a campaign that has started.
          CANNOT_SET_DATE_TO_PAST (int): Trying to modify a date into the past.
          MISSING_HOTEL_CUSTOMER_LINK (int): Hotel center id in the hotel setting does not match any customer links.
          INVALID_HOTEL_CUSTOMER_LINK (int): Hotel center id in the hotel setting must match an active customer link.
          MISSING_HOTEL_SETTING (int): Hotel setting was not found when creating a hotel ads campaign.
          CANNOT_USE_SHARED_CAMPAIGN_BUDGET_WHILE_PART_OF_CAMPAIGN_GROUP (int): A Campaign cannot use shared campaign budgets and be part of a campaign
          group.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CANNOT_TARGET_CONTENT_NETWORK = 3
        CANNOT_TARGET_SEARCH_NETWORK = 4
        CANNOT_TARGET_SEARCH_NETWORK_WITHOUT_GOOGLE_SEARCH = 5
        CANNOT_TARGET_GOOGLE_SEARCH_FOR_CPM_CAMPAIGN = 6
        CAMPAIGN_MUST_TARGET_AT_LEAST_ONE_NETWORK = 7
        CANNOT_TARGET_PARTNER_SEARCH_NETWORK = 8
        CANNOT_TARGET_CONTENT_NETWORK_ONLY_WITH_CRITERIA_LEVEL_BIDDING_STRATEGY = 9
        CAMPAIGN_DURATION_MUST_CONTAIN_ALL_RUNNABLE_TRIALS = 10
        CANNOT_MODIFY_FOR_TRIAL_CAMPAIGN = 11
        DUPLICATE_CAMPAIGN_NAME = 12
        INCOMPATIBLE_CAMPAIGN_FIELD = 13
        INVALID_CAMPAIGN_NAME = 14
        INVALID_AD_SERVING_OPTIMIZATION_STATUS = 15
        INVALID_TRACKING_URL = 16
        CANNOT_SET_BOTH_TRACKING_URL_TEMPLATE_AND_TRACKING_SETTING = 17
        MAX_IMPRESSIONS_NOT_IN_RANGE = 18
        TIME_UNIT_NOT_SUPPORTED = 19
        INVALID_OPERATION_IF_SERVING_STATUS_HAS_ENDED = 20
        BUDGET_CANNOT_BE_SHARED = 21
        CAMPAIGN_CANNOT_USE_SHARED_BUDGET = 22
        CANNOT_CHANGE_BUDGET_ON_CAMPAIGN_WITH_TRIALS = 23
        CAMPAIGN_LABEL_DOES_NOT_EXIST = 24
        CAMPAIGN_LABEL_ALREADY_EXISTS = 25
        MISSING_SHOPPING_SETTING = 26
        INVALID_SHOPPING_SALES_COUNTRY = 27
        MISSING_UNIVERSAL_APP_CAMPAIGN_SETTING = 30
        ADVERTISING_CHANNEL_TYPE_NOT_AVAILABLE_FOR_ACCOUNT_TYPE = 31
        INVALID_ADVERTISING_CHANNEL_SUB_TYPE = 32
        AT_LEAST_ONE_CONVERSION_MUST_BE_SELECTED = 33
        CANNOT_SET_AD_ROTATION_MODE = 34
        CANNOT_MODIFY_START_DATE_IF_ALREADY_STARTED = 35
        CANNOT_SET_DATE_TO_PAST = 36
        MISSING_HOTEL_CUSTOMER_LINK = 37
        INVALID_HOTEL_CUSTOMER_LINK = 38
        MISSING_HOTEL_SETTING = 39
        CANNOT_USE_SHARED_CAMPAIGN_BUDGET_WHILE_PART_OF_CAMPAIGN_GROUP = 40


class CampaignGroupErrorEnum(object):
    class CampaignGroupError(enum.IntEnum):
        """
        Enum describing possible campaign group errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CANNOT_REMOVE_CAMPAIGN_GROUP_WITH_ENABLED_OR_PAUSED_CAMPAIGNS (int): CampaignGroup was removed with ENABLED or PAUSED Campaigns associated
          with it.
          DUPLICATE_NAME (int): CampaignGroup with the given name already exists.
          CANNOT_MODIFY_REMOVED_CAMPAIGN_GROUP (int): Cannot modify a removed campaign group.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CANNOT_REMOVE_CAMPAIGN_GROUP_WITH_ENABLED_OR_PAUSED_CAMPAIGNS = 2
        DUPLICATE_NAME = 3
        CANNOT_MODIFY_REMOVED_CAMPAIGN_GROUP = 4


class CollectionSizeErrorEnum(object):
    class CollectionSizeError(enum.IntEnum):
        """
        Enum describing possible collection size errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          TOO_FEW (int): Too few.
          TOO_MANY (int): Too many.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        TOO_FEW = 2
        TOO_MANY = 3


class ContextErrorEnum(object):
    class ContextError(enum.IntEnum):
        """
        Enum describing possible context errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          OPERATION_NOT_PERMITTED_FOR_CONTEXT (int): The operation is not allowed for the given context.
          OPERATION_NOT_PERMITTED_FOR_REMOVED_RESOURCE (int): The operation is not allowed for removed resources.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        OPERATION_NOT_PERMITTED_FOR_CONTEXT = 2
        OPERATION_NOT_PERMITTED_FOR_REMOVED_RESOURCE = 3


class CriterionErrorEnum(object):
    class CriterionError(enum.IntEnum):
        """
        Enum describing possible criterion errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CONCRETE_TYPE_REQUIRED (int): Concrete type of criterion is required for CREATE and UPDATE operations.
          INVALID_EXCLUDED_CATEGORY (int): The category requested for exclusion is invalid.
          INVALID_KEYWORD_TEXT (int): Invalid keyword criteria text.
          KEYWORD_TEXT_TOO_LONG (int): Keyword text should be less than 80 chars.
          KEYWORD_HAS_TOO_MANY_WORDS (int): Keyword text has too many words.
          KEYWORD_HAS_INVALID_CHARS (int): Keyword text has invalid characters or symbols.
          INVALID_PLACEMENT_URL (int): Invalid placement URL.
          INVALID_USER_LIST (int): Invalid user list criterion.
          INVALID_USER_INTEREST (int): Invalid user interest criterion.
          INVALID_FORMAT_FOR_PLACEMENT_URL (int): Placement URL has wrong format.
          PLACEMENT_URL_IS_TOO_LONG (int): Placement URL is too long.
          PLACEMENT_URL_HAS_ILLEGAL_CHAR (int): Indicates the URL contains an illegal character.
          PLACEMENT_URL_HAS_MULTIPLE_SITES_IN_LINE (int): Indicates the URL contains multiple comma separated URLs.
          PLACEMENT_IS_NOT_AVAILABLE_FOR_TARGETING_OR_EXCLUSION (int): Indicates the domain is blacklisted.
          INVALID_TOPIC_PATH (int): Invalid topic path.
          INVALID_YOUTUBE_CHANNEL_ID (int): The YouTube Channel Id is invalid.
          INVALID_YOUTUBE_VIDEO_ID (int): The YouTube Video Id is invalid.
          YOUTUBE_VERTICAL_CHANNEL_DEPRECATED (int): Indicates the placement is a YouTube vertical channel, which is no longer
          supported.
          YOUTUBE_DEMOGRAPHIC_CHANNEL_DEPRECATED (int): Indicates the placement is a YouTube demographic channel, which is no
          longer supported.
          YOUTUBE_URL_UNSUPPORTED (int): YouTube urls are not supported in Placement criterion. Use YouTubeChannel
          and YouTubeVideo criterion instead.
          CANNOT_EXCLUDE_CRITERIA_TYPE (int): Criteria type can not be excluded by the customer, like AOL account type
          cannot target site type criteria.
          CANNOT_ADD_CRITERIA_TYPE (int): Criteria type can not be targeted.
          INVALID_PRODUCT_FILTER (int): Product filter in the product criteria has invalid characters. Operand
          and the argument in the filter can not have \"==\" or \"&+\".
          PRODUCT_FILTER_TOO_LONG (int): Product filter in the product criteria is translated to a string as
          operand1==argument1&+operand2==argument2, maximum allowed length for the
          string is 255 chars.
          CANNOT_EXCLUDE_SIMILAR_USER_LIST (int): Not allowed to exclude similar user list.
          CANNOT_ADD_CLOSED_USER_LIST (int): Not allowed to target a closed user list.
          CANNOT_ADD_DISPLAY_ONLY_LISTS_TO_SEARCH_ONLY_CAMPAIGNS (int): Not allowed to add display only UserLists to search only campaigns.
          CANNOT_ADD_DISPLAY_ONLY_LISTS_TO_SEARCH_CAMPAIGNS (int): Not allowed to add display only UserLists to search plus campaigns.
          CANNOT_ADD_DISPLAY_ONLY_LISTS_TO_SHOPPING_CAMPAIGNS (int): Not allowed to add display only UserLists to shopping campaigns.
          CANNOT_ADD_USER_INTERESTS_TO_SEARCH_CAMPAIGNS (int): Not allowed to add User interests to search only campaigns.
          CANNOT_SET_BIDS_ON_CRITERION_TYPE_IN_SEARCH_CAMPAIGNS (int): Not allowed to set bids for this criterion type in search campaigns
          CANNOT_ADD_URLS_TO_CRITERION_TYPE_FOR_CAMPAIGN_TYPE (int): Final URLs, URL Templates and CustomParameters cannot be set for the
          criterion types of Gender, AgeRange, UserList, Placement, MobileApp, and
          MobileAppCategory in search campaigns and shopping campaigns.
          INVALID_IP_ADDRESS (int): IP address is not valid.
          INVALID_IP_FORMAT (int): IP format is not valid.
          INVALID_MOBILE_APP (int): Mobile application is not valid.
          INVALID_MOBILE_APP_CATEGORY (int): Mobile application category is not valid.
          INVALID_CRITERION_ID (int): The CriterionId does not exist or is of the incorrect type.
          CANNOT_TARGET_CRITERION (int): The Criterion is not allowed to be targeted.
          CANNOT_TARGET_OBSOLETE_CRITERION (int): The criterion is not allowed to be targeted as it is deprecated.
          CRITERION_ID_AND_TYPE_MISMATCH (int): The CriterionId is not valid for the type.
          INVALID_PROXIMITY_RADIUS (int): Distance for the radius for the proximity criterion is invalid.
          INVALID_PROXIMITY_RADIUS_UNITS (int): Units for the distance for the radius for the proximity criterion is
          invalid.
          INVALID_STREETADDRESS_LENGTH (int): Street address in the address is not valid.
          INVALID_CITYNAME_LENGTH (int): City name in the address is not valid.
          INVALID_REGIONCODE_LENGTH (int): Region code in the address is not valid.
          INVALID_REGIONNAME_LENGTH (int): Region name in the address is not valid.
          INVALID_POSTALCODE_LENGTH (int): Postal code in the address is not valid.
          INVALID_COUNTRY_CODE (int): Country code in the address is not valid.
          INVALID_LATITUDE (int): Latitude for the GeoPoint is not valid.
          INVALID_LONGITUDE (int): Longitude for the GeoPoint is not valid.
          PROXIMITY_GEOPOINT_AND_ADDRESS_BOTH_CANNOT_BE_NULL (int): The Proximity input is not valid. Both address and geoPoint cannot be
          null.
          INVALID_PROXIMITY_ADDRESS (int): The Proximity address cannot be geocoded to a valid lat/long.
          INVALID_USER_DOMAIN_NAME (int): User domain name is not valid.
          CRITERION_PARAMETER_TOO_LONG (int): Length of serialized criterion parameter exceeded size limit.
          AD_SCHEDULE_TIME_INTERVALS_OVERLAP (int): Time interval in the AdSchedule overlaps with another AdSchedule.
          AD_SCHEDULE_INTERVAL_CANNOT_SPAN_MULTIPLE_DAYS (int): AdSchedule time interval cannot span multiple days.
          AD_SCHEDULE_INVALID_TIME_INTERVAL (int): AdSchedule time interval specified is invalid, endTime cannot be earlier
          than startTime.
          AD_SCHEDULE_EXCEEDED_INTERVALS_PER_DAY_LIMIT (int): The number of AdSchedule entries in a day exceeds the limit.
          AD_SCHEDULE_CRITERION_ID_MISMATCHING_FIELDS (int): CriteriaId does not match the interval of the AdSchedule specified.
          CANNOT_BID_MODIFY_CRITERION_TYPE (int): Cannot set bid modifier for this criterion type.
          CANNOT_BID_MODIFY_CRITERION_CAMPAIGN_OPTED_OUT (int): Cannot bid modify criterion, since it is opted out of the campaign.
          CANNOT_BID_MODIFY_NEGATIVE_CRITERION (int): Cannot set bid modifier for a negative criterion.
          BID_MODIFIER_ALREADY_EXISTS (int): Bid Modifier already exists. Use SET operation to update.
          FEED_ID_NOT_ALLOWED (int): Feed Id is not allowed in these Location Groups.
          ACCOUNT_INELIGIBLE_FOR_CRITERIA_TYPE (int): The account may not use the requested criteria type. For example, some
          accounts are restricted to keywords only.
          CRITERIA_TYPE_INVALID_FOR_BIDDING_STRATEGY (int): The requested criteria type cannot be used with campaign or ad group
          bidding strategy.
          CANNOT_EXCLUDE_CRITERION (int): The Criterion is not allowed to be excluded.
          CANNOT_REMOVE_CRITERION (int): The criterion is not allowed to be removed. For example, we cannot remove
          any of the device criterion.
          PRODUCT_SCOPE_TOO_LONG (int): The combined length of product dimension values of the product scope
          criterion is too long.
          PRODUCT_SCOPE_TOO_MANY_DIMENSIONS (int): Product scope contains too many dimensions.
          PRODUCT_PARTITION_TOO_LONG (int): The combined length of product dimension values of the product partition
          criterion is too long.
          PRODUCT_PARTITION_TOO_MANY_DIMENSIONS (int): Product partition contains too many dimensions.
          INVALID_PRODUCT_DIMENSION (int): The product dimension is invalid (e.g. dimension contains illegal value,
          dimension type is represented with wrong class, etc). Product dimension
          value can not contain \"==\" or \"&+\".
          INVALID_PRODUCT_DIMENSION_TYPE (int): Product dimension type is either invalid for campaigns of this type or
          cannot be used in the current context. BIDDING_CATEGORY_Lx and
          PRODUCT_TYPE_Lx product dimensions must be used in ascending order of
          their levels: L1, L2, L3, L4, L5... The levels must be specified
          sequentially and start from L1. Furthermore, an \"others\" product
          partition cannot be subdivided with a dimension of the same type but of a
          higher level (\"others\" BIDDING_CATEGORY_L3 can be subdivided with BRAND
          but not with BIDDING_CATEGORY_L4).
          INVALID_PRODUCT_BIDDING_CATEGORY (int): Bidding categories do not form a valid path in the Shopping bidding
          category taxonomy.
          MISSING_SHOPPING_SETTING (int): ShoppingSetting must be added to the campaign before ProductScope
          criteria can be added.
          INVALID_MATCHING_FUNCTION (int): Matching function is invalid.
          LOCATION_FILTER_NOT_ALLOWED (int): Filter parameters not allowed for location groups targeting.
          LOCATION_FILTER_INVALID (int): Given location filter parameter is invalid for location groups targeting.
          CANNOT_ATTACH_CRITERIA_AT_CAMPAIGN_AND_ADGROUP (int): Criteria type cannot be associated with a campaign and its ad group(s)
          simultaneously.
          HOTEL_LENGTH_OF_STAY_OVERLAPS_WITH_EXISTING_CRITERION (int): Range represented by hotel length of stay's min nights and max nights
          overlaps with an existing criterion.
          HOTEL_ADVANCE_BOOKING_WINDOW_OVERLAPS_WITH_EXISTING_CRITERION (int): Range represented by hotel advance booking window's min days and max days
          overlaps with an existing criterion.
          FIELD_INCOMPATIBLE_WITH_NEGATIVE_TARGETING (int): The field is not allowed to be set when the negative field is set to
          true, e.g. we don't allow bids in negative ad group or campaign criteria.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CONCRETE_TYPE_REQUIRED = 2
        INVALID_EXCLUDED_CATEGORY = 3
        INVALID_KEYWORD_TEXT = 4
        KEYWORD_TEXT_TOO_LONG = 5
        KEYWORD_HAS_TOO_MANY_WORDS = 6
        KEYWORD_HAS_INVALID_CHARS = 7
        INVALID_PLACEMENT_URL = 8
        INVALID_USER_LIST = 9
        INVALID_USER_INTEREST = 10
        INVALID_FORMAT_FOR_PLACEMENT_URL = 11
        PLACEMENT_URL_IS_TOO_LONG = 12
        PLACEMENT_URL_HAS_ILLEGAL_CHAR = 13
        PLACEMENT_URL_HAS_MULTIPLE_SITES_IN_LINE = 14
        PLACEMENT_IS_NOT_AVAILABLE_FOR_TARGETING_OR_EXCLUSION = 15
        INVALID_TOPIC_PATH = 16
        INVALID_YOUTUBE_CHANNEL_ID = 17
        INVALID_YOUTUBE_VIDEO_ID = 18
        YOUTUBE_VERTICAL_CHANNEL_DEPRECATED = 19
        YOUTUBE_DEMOGRAPHIC_CHANNEL_DEPRECATED = 20
        YOUTUBE_URL_UNSUPPORTED = 21
        CANNOT_EXCLUDE_CRITERIA_TYPE = 22
        CANNOT_ADD_CRITERIA_TYPE = 23
        INVALID_PRODUCT_FILTER = 24
        PRODUCT_FILTER_TOO_LONG = 25
        CANNOT_EXCLUDE_SIMILAR_USER_LIST = 26
        CANNOT_ADD_CLOSED_USER_LIST = 27
        CANNOT_ADD_DISPLAY_ONLY_LISTS_TO_SEARCH_ONLY_CAMPAIGNS = 28
        CANNOT_ADD_DISPLAY_ONLY_LISTS_TO_SEARCH_CAMPAIGNS = 29
        CANNOT_ADD_DISPLAY_ONLY_LISTS_TO_SHOPPING_CAMPAIGNS = 30
        CANNOT_ADD_USER_INTERESTS_TO_SEARCH_CAMPAIGNS = 31
        CANNOT_SET_BIDS_ON_CRITERION_TYPE_IN_SEARCH_CAMPAIGNS = 32
        CANNOT_ADD_URLS_TO_CRITERION_TYPE_FOR_CAMPAIGN_TYPE = 33
        INVALID_IP_ADDRESS = 34
        INVALID_IP_FORMAT = 35
        INVALID_MOBILE_APP = 36
        INVALID_MOBILE_APP_CATEGORY = 37
        INVALID_CRITERION_ID = 38
        CANNOT_TARGET_CRITERION = 39
        CANNOT_TARGET_OBSOLETE_CRITERION = 40
        CRITERION_ID_AND_TYPE_MISMATCH = 41
        INVALID_PROXIMITY_RADIUS = 42
        INVALID_PROXIMITY_RADIUS_UNITS = 43
        INVALID_STREETADDRESS_LENGTH = 44
        INVALID_CITYNAME_LENGTH = 45
        INVALID_REGIONCODE_LENGTH = 46
        INVALID_REGIONNAME_LENGTH = 47
        INVALID_POSTALCODE_LENGTH = 48
        INVALID_COUNTRY_CODE = 49
        INVALID_LATITUDE = 50
        INVALID_LONGITUDE = 51
        PROXIMITY_GEOPOINT_AND_ADDRESS_BOTH_CANNOT_BE_NULL = 52
        INVALID_PROXIMITY_ADDRESS = 53
        INVALID_USER_DOMAIN_NAME = 54
        CRITERION_PARAMETER_TOO_LONG = 55
        AD_SCHEDULE_TIME_INTERVALS_OVERLAP = 56
        AD_SCHEDULE_INTERVAL_CANNOT_SPAN_MULTIPLE_DAYS = 57
        AD_SCHEDULE_INVALID_TIME_INTERVAL = 58
        AD_SCHEDULE_EXCEEDED_INTERVALS_PER_DAY_LIMIT = 59
        AD_SCHEDULE_CRITERION_ID_MISMATCHING_FIELDS = 60
        CANNOT_BID_MODIFY_CRITERION_TYPE = 61
        CANNOT_BID_MODIFY_CRITERION_CAMPAIGN_OPTED_OUT = 62
        CANNOT_BID_MODIFY_NEGATIVE_CRITERION = 63
        BID_MODIFIER_ALREADY_EXISTS = 64
        FEED_ID_NOT_ALLOWED = 65
        ACCOUNT_INELIGIBLE_FOR_CRITERIA_TYPE = 66
        CRITERIA_TYPE_INVALID_FOR_BIDDING_STRATEGY = 67
        CANNOT_EXCLUDE_CRITERION = 68
        CANNOT_REMOVE_CRITERION = 69
        PRODUCT_SCOPE_TOO_LONG = 70
        PRODUCT_SCOPE_TOO_MANY_DIMENSIONS = 71
        PRODUCT_PARTITION_TOO_LONG = 72
        PRODUCT_PARTITION_TOO_MANY_DIMENSIONS = 73
        INVALID_PRODUCT_DIMENSION = 74
        INVALID_PRODUCT_DIMENSION_TYPE = 75
        INVALID_PRODUCT_BIDDING_CATEGORY = 76
        MISSING_SHOPPING_SETTING = 77
        INVALID_MATCHING_FUNCTION = 78
        LOCATION_FILTER_NOT_ALLOWED = 79
        LOCATION_FILTER_INVALID = 80
        CANNOT_ATTACH_CRITERIA_AT_CAMPAIGN_AND_ADGROUP = 81
        HOTEL_LENGTH_OF_STAY_OVERLAPS_WITH_EXISTING_CRITERION = 82
        HOTEL_ADVANCE_BOOKING_WINDOW_OVERLAPS_WITH_EXISTING_CRITERION = 83
        FIELD_INCOMPATIBLE_WITH_NEGATIVE_TARGETING = 84


class CustomerClientLinkErrorEnum(object):
    class CustomerClientLinkError(enum.IntEnum):
        """
        Enum describing possible CustomerClientLink errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CLIENT_ALREADY_INVITED_BY_THIS_MANAGER (int): Trying to manage a client that already in being managed by customer.
          CLIENT_ALREADY_MANAGED_IN_HIERARCHY (int): Already managed by some other manager in the hierarchy.
          CYCLIC_LINK_NOT_ALLOWED (int): Attempt to create a cycle in the hierarchy.
          CUSTOMER_HAS_TOO_MANY_ACCOUNTS (int): Managed accounts has the maximum number of linked accounts.
          CLIENT_HAS_TOO_MANY_INVITATIONS (int): Invitor has the maximum pending invitations.
          CANNOT_HIDE_OR_UNHIDE_MANAGER_ACCOUNTS (int): Attempt to change hidden status of a link that is not active.
          CUSTOMER_HAS_TOO_MANY_ACCOUNTS_AT_MANAGER (int): Parent manager account has the maximum number of linked accounts.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CLIENT_ALREADY_INVITED_BY_THIS_MANAGER = 2
        CLIENT_ALREADY_MANAGED_IN_HIERARCHY = 3
        CYCLIC_LINK_NOT_ALLOWED = 4
        CUSTOMER_HAS_TOO_MANY_ACCOUNTS = 5
        CLIENT_HAS_TOO_MANY_INVITATIONS = 6
        CANNOT_HIDE_OR_UNHIDE_MANAGER_ACCOUNTS = 7
        CUSTOMER_HAS_TOO_MANY_ACCOUNTS_AT_MANAGER = 8


class CustomerErrorEnum(object):
    class CustomerError(enum.IntEnum):
        """
        Set of errors that are related to requests dealing with Customer.
        Next id: 26

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          STATUS_CHANGE_DISALLOWED (int): Customer status is not allowed to be changed from DRAFT and CLOSED.
          Currency code and at least one of country code and time zone needs to be
          set when status is changed to ENABLED.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        STATUS_CHANGE_DISALLOWED = 2


class DatabaseErrorEnum(object):
    class DatabaseError(enum.IntEnum):
        """
        Enum describing possible database errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CONCURRENT_MODIFICATION (int): Multiple requests were attempting to modify the same resource at once.
          Please retry the request.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CONCURRENT_MODIFICATION = 2


class DateRangeErrorEnum(object):
    class DateRangeError(enum.IntEnum):
        """
        Enum describing possible date range errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          INVALID_DATE (int): Invalid date.
          START_DATE_AFTER_END_DATE (int): The start date was after the end date.
          CANNOT_SET_DATE_TO_PAST (int): Cannot set date to past time
          AFTER_MAXIMUM_ALLOWABLE_DATE (int): A date was used that is past the system \"last\" date.
          CANNOT_MODIFY_START_DATE_IF_ALREADY_STARTED (int): Trying to change start date on a campaign that has started.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INVALID_DATE = 2
        START_DATE_AFTER_END_DATE = 3
        CANNOT_SET_DATE_TO_PAST = 4
        AFTER_MAXIMUM_ALLOWABLE_DATE = 5
        CANNOT_MODIFY_START_DATE_IF_ALREADY_STARTED = 6


class FunctionErrorEnum(object):
    class FunctionError(enum.IntEnum):
        """
        Enum describing possible function errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          INVALID_FUNCTION_FORMAT (int): The format of the function is not recognized as a supported function
          format.
          DATA_TYPE_MISMATCH (int): Operand data types do not match.
          INVALID_CONJUNCTION_OPERANDS (int): The operands cannot be used together in a conjunction.
          INVALID_NUMBER_OF_OPERANDS (int): Invalid numer of Operands.
          INVALID_OPERAND_TYPE (int): Operand Type not supported.
          INVALID_OPERATOR (int): Operator not supported.
          INVALID_REQUEST_CONTEXT_TYPE (int): Request context type not supported.
          INVALID_FUNCTION_FOR_CALL_PLACEHOLDER (int): The matching function is not allowed for call placeholders
          INVALID_FUNCTION_FOR_PLACEHOLDER (int): The matching function is not allowed for the specified placeholder
          INVALID_OPERAND (int): Invalid operand.
          MISSING_CONSTANT_OPERAND_VALUE (int): Missing value for the constant operand.
          INVALID_CONSTANT_OPERAND_VALUE (int): The value of the constant operand is invalid.
          INVALID_NESTING (int): Invalid function nesting.
          MULTIPLE_FEED_IDS_NOT_SUPPORTED (int): The Feed ID was different from another Feed ID in the same function.
          INVALID_FUNCTION_FOR_FEED_WITH_FIXED_SCHEMA (int): The matching function is invalid for use with a feed with a fixed schema.
          INVALID_ATTRIBUTE_NAME (int): Invalid attribute name.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INVALID_FUNCTION_FORMAT = 2
        DATA_TYPE_MISMATCH = 3
        INVALID_CONJUNCTION_OPERANDS = 4
        INVALID_NUMBER_OF_OPERANDS = 5
        INVALID_OPERAND_TYPE = 6
        INVALID_OPERATOR = 7
        INVALID_REQUEST_CONTEXT_TYPE = 8
        INVALID_FUNCTION_FOR_CALL_PLACEHOLDER = 9
        INVALID_FUNCTION_FOR_PLACEHOLDER = 10
        INVALID_OPERAND = 11
        MISSING_CONSTANT_OPERAND_VALUE = 12
        INVALID_CONSTANT_OPERAND_VALUE = 13
        INVALID_NESTING = 14
        MULTIPLE_FEED_IDS_NOT_SUPPORTED = 15
        INVALID_FUNCTION_FOR_FEED_WITH_FIXED_SCHEMA = 16
        INVALID_ATTRIBUTE_NAME = 17


class FunctionParsingErrorEnum(object):
    class FunctionParsingError(enum.IntEnum):
        """
        Enum describing possible function parsing errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          NO_MORE_INPUT (int): Unexpected end of function string.
          EXPECTED_CHARACTER (int): Could not find an expected character.
          UNEXPECTED_SEPARATOR (int): Unexpected separator character.
          UNMATCHED_LEFT_BRACKET (int): Unmatched left bracket or parenthesis.
          UNMATCHED_RIGHT_BRACKET (int): Unmatched right bracket or parenthesis.
          TOO_MANY_NESTED_FUNCTIONS (int): Functions are nested too deeply.
          MISSING_RIGHT_HAND_OPERAND (int): Missing right-hand-side operand.
          INVALID_OPERATOR_NAME (int): Invalid operator/function name.
          FEED_ATTRIBUTE_OPERAND_ARGUMENT_NOT_INTEGER (int): Feed attribute operand's argument is not an integer.
          NO_OPERANDS (int): Missing function operands.
          TOO_MANY_OPERANDS (int): Function had too many operands.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        NO_MORE_INPUT = 2
        EXPECTED_CHARACTER = 3
        UNEXPECTED_SEPARATOR = 4
        UNMATCHED_LEFT_BRACKET = 5
        UNMATCHED_RIGHT_BRACKET = 6
        TOO_MANY_NESTED_FUNCTIONS = 7
        MISSING_RIGHT_HAND_OPERAND = 8
        INVALID_OPERATOR_NAME = 9
        FEED_ATTRIBUTE_OPERAND_ARGUMENT_NOT_INTEGER = 10
        NO_OPERANDS = 11
        TOO_MANY_OPERANDS = 12


class GeoTargetConstantSuggestionErrorEnum(object):
    class GeoTargetConstantSuggestionError(enum.IntEnum):
        """
        Enum describing possible geo target constant suggestion errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          LOCATION_NAME_SIZE_LIMIT (int): A location name cannot be greater than 300 characters.
          LOCATION_NAME_LIMIT (int): At most 25 location names can be specified in a SuggestGeoTargetConstants
          method.
          INVALID_COUNTRY_CODE (int): The country code is invalid.
          REQUEST_PARAMETERS_UNSET (int): Geo target constant resource names or location names must be provided in
          the request.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        LOCATION_NAME_SIZE_LIMIT = 2
        LOCATION_NAME_LIMIT = 3
        INVALID_COUNTRY_CODE = 4
        REQUEST_PARAMETERS_UNSET = 5


class HeaderErrorEnum(object):
    class HeaderError(enum.IntEnum):
        """
        Enum describing possible header errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          INVALID_LOGIN_CUSTOMER_ID (int): The login customer id could not be validated.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INVALID_LOGIN_CUSTOMER_ID = 3


class IdErrorEnum(object):
    class IdError(enum.IntEnum):
        """
        Enum describing possible id errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          NOT_FOUND (int): Id not found
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        NOT_FOUND = 2


class MultiplierErrorEnum(object):
    class MultiplierError(enum.IntEnum):
        """
        Enum describing possible multiplier errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          MULTIPLIER_TOO_HIGH (int): Multiplier value is too high
          MULTIPLIER_TOO_LOW (int): Multiplier value is too low
          TOO_MANY_FRACTIONAL_DIGITS (int): Too many fractional digits
          MULTIPLIER_NOT_ALLOWED_FOR_BIDDING_STRATEGY (int): A multiplier cannot be set for this bidding strategy
          MULTIPLIER_NOT_ALLOWED_WHEN_BASE_BID_IS_MISSING (int): A multiplier cannot be set when there is no base bid (e.g., content max
          cpc)
          NO_MULTIPLIER_SPECIFIED (int): A bid multiplier must be specified
          MULTIPLIER_CAUSES_BID_TO_EXCEED_DAILY_BUDGET (int): Multiplier causes bid to exceed daily budget
          MULTIPLIER_CAUSES_BID_TO_EXCEED_MONTHLY_BUDGET (int): Multiplier causes bid to exceed monthly budget
          MULTIPLIER_CAUSES_BID_TO_EXCEED_CUSTOM_BUDGET (int): Multiplier causes bid to exceed custom budget
          MULTIPLIER_CAUSES_BID_TO_EXCEED_MAX_ALLOWED_BID (int): Multiplier causes bid to exceed maximum allowed bid
          BID_LESS_THAN_MIN_ALLOWED_BID_WITH_MULTIPLIER (int): Multiplier causes bid to become less than the minimum bid allowed
          MULTIPLIER_AND_BIDDING_STRATEGY_TYPE_MISMATCH (int): Multiplier type (cpc vs. cpm) needs to match campaign's bidding strategy
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        MULTIPLIER_TOO_HIGH = 2
        MULTIPLIER_TOO_LOW = 3
        TOO_MANY_FRACTIONAL_DIGITS = 4
        MULTIPLIER_NOT_ALLOWED_FOR_BIDDING_STRATEGY = 5
        MULTIPLIER_NOT_ALLOWED_WHEN_BASE_BID_IS_MISSING = 6
        NO_MULTIPLIER_SPECIFIED = 7
        MULTIPLIER_CAUSES_BID_TO_EXCEED_DAILY_BUDGET = 8
        MULTIPLIER_CAUSES_BID_TO_EXCEED_MONTHLY_BUDGET = 9
        MULTIPLIER_CAUSES_BID_TO_EXCEED_CUSTOM_BUDGET = 10
        MULTIPLIER_CAUSES_BID_TO_EXCEED_MAX_ALLOWED_BID = 11
        BID_LESS_THAN_MIN_ALLOWED_BID_WITH_MULTIPLIER = 12
        MULTIPLIER_AND_BIDDING_STRATEGY_TYPE_MISMATCH = 13


class MutateErrorEnum(object):
    class MutateError(enum.IntEnum):
        """
        Enum describing possible mutate errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          RESOURCE_NOT_FOUND (int): Requested resource was not found.
          ID_EXISTS_IN_MULTIPLE_MUTATES (int): Cannot mutate the same resource twice in one request.
          INCONSISTENT_FIELD_VALUES (int): The field's contents don't match another field that represents the same
          data.
          MUTATE_NOT_ALLOWED (int): Mutates are not allowed for the requested resource.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        RESOURCE_NOT_FOUND = 3
        ID_EXISTS_IN_MULTIPLE_MUTATES = 7
        INCONSISTENT_FIELD_VALUES = 8
        MUTATE_NOT_ALLOWED = 9


class NewResourceCreationErrorEnum(object):
    class NewResourceCreationError(enum.IntEnum):
        """
        Enum describing possible new resource creation errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CANNOT_SET_ID_FOR_ADD (int): Do not set the id field while creating new entities.
          DUPLICATE_TEMP_IDS (int): Creating more than one resource with the same temp ID is not allowed.
          TEMP_ID_RESOURCE_HAD_ERRORS (int): Parent object with specified temp id failed validation, so no deep
          validation will be done for this child resource.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CANNOT_SET_ID_FOR_ADD = 2
        DUPLICATE_TEMP_IDS = 3
        TEMP_ID_RESOURCE_HAD_ERRORS = 4


class NotEmptyErrorEnum(object):
    class NotEmptyError(enum.IntEnum):
        """
        Enum describing possible not empty errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          EMPTY_LIST (int): Empty list.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        EMPTY_LIST = 2


class NullErrorEnum(object):
    class NullError(enum.IntEnum):
        """
        Enum describing possible null errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          NULL_CONTENT (int): Specified list/container must not contain any null elements
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        NULL_CONTENT = 2


class OperationAccessDeniedErrorEnum(object):
    class OperationAccessDeniedError(enum.IntEnum):
        """
        Enum describing possible operation access denied errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          ACTION_NOT_PERMITTED (int): Unauthorized invocation of a service's method (get, mutate, etc.)
          CREATE_OPERATION_NOT_PERMITTED (int): Unauthorized CREATE operation in invoking a service's mutate method.
          REMOVE_OPERATION_NOT_PERMITTED (int): Unauthorized REMOVE operation in invoking a service's mutate method.
          UPDATE_OPERATION_NOT_PERMITTED (int): Unauthorized UPDATE operation in invoking a service's mutate method.
          MUTATE_ACTION_NOT_PERMITTED_FOR_CLIENT (int): A mutate action is not allowed on this campaign, from this client.
          OPERATION_NOT_PERMITTED_FOR_CAMPAIGN_TYPE (int): This operation is not permitted on this campaign type
          CREATE_AS_REMOVED_NOT_PERMITTED (int): A CREATE operation may not set status to REMOVED.
          OPERATION_NOT_PERMITTED_FOR_REMOVED_RESOURCE (int): This operation is not allowed because the campaign or adgroup is removed.
          OPERATION_NOT_PERMITTED_FOR_AD_GROUP_TYPE (int): This operation is not permitted on this ad group type.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ACTION_NOT_PERMITTED = 2
        CREATE_OPERATION_NOT_PERMITTED = 3
        REMOVE_OPERATION_NOT_PERMITTED = 4
        UPDATE_OPERATION_NOT_PERMITTED = 5
        MUTATE_ACTION_NOT_PERMITTED_FOR_CLIENT = 6
        OPERATION_NOT_PERMITTED_FOR_CAMPAIGN_TYPE = 7
        CREATE_AS_REMOVED_NOT_PERMITTED = 8
        OPERATION_NOT_PERMITTED_FOR_REMOVED_RESOURCE = 9
        OPERATION_NOT_PERMITTED_FOR_AD_GROUP_TYPE = 10


class OperatorErrorEnum(object):
    class OperatorError(enum.IntEnum):
        """
        Enum describing possible operator errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          OPERATOR_NOT_SUPPORTED (int): Operator not supported.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        OPERATOR_NOT_SUPPORTED = 2


class QueryErrorEnum(object):
    class QueryError(enum.IntEnum):
        """
        Enum describing possible query errors.

        Attributes:
          UNSPECIFIED (int): Name unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          QUERY_ERROR (int): Returned if all other query error reasons are not applicable.
          BAD_ENUM_CONSTANT (int): A condition used in the query references an invalid enum constant.
          BAD_ESCAPE_SEQUENCE (int): Query contains an invalid escape sequence.
          BAD_FIELD_NAME (int): Field name is invalid.
          BAD_LIMIT_VALUE (int): Limit value is invalid (i.e. not a number)
          BAD_NUMBER (int): Encountered number can not be parsed.
          BAD_OPERATOR (int): Invalid operator encountered.
          BAD_RESOURCE_TYPE_IN_FROM_CLAUSE (int): Invalid resource type was specified in the FROM clause.
          BAD_SYMBOL (int): Non-ASCII symbol encountered outside of strings.
          BAD_VALUE (int): Value is invalid.
          DATE_RANGE_TOO_WIDE (int): Date filters fail to restrict date to a range smaller than 31 days.
          Applicable if the query is segmented by date.
          EXPECTED_AND (int): Expected AND between values with BETWEEN operator.
          EXPECTED_BY (int): Expecting ORDER BY to have BY.
          EXPECTED_DIMENSION_FIELD_IN_SELECT_CLAUSE (int): There was no dimension field selected.
          EXPECTED_FILTERS_ON_DATE_RANGE (int): Missing filters on date related fields.
          EXPECTED_FROM (int): Missing FROM clause.
          EXPECTED_LIST (int): The operator used in the conditions requires the value to be a list.
          EXPECTED_REFERENCED_FIELD_IN_SELECT_CLAUSE (int): Fields used in WHERE or ORDER BY clauses are missing from the SELECT
          clause.
          EXPECTED_SELECT (int): SELECT is missing at the beginning of query.
          EXPECTED_SINGLE_VALUE (int): A list was passed as a value to a condition whose operator expects a
          single value.
          EXPECTED_VALUE_WITH_BETWEEN_OPERATOR (int): Missing one or both values with BETWEEN operator.
          INVALID_DATE_FORMAT (int): Invalid date format. Expected 'YYYY-MM-DD'.
          INVALID_STRING_VALUE (int): Value passed was not a string when it should have been. I.e., it was a
          number or unquoted literal.
          INVALID_VALUE_WITH_BETWEEN_OPERATOR (int): A String value passed to the BETWEEN operator does not parse as a date.
          INVALID_VALUE_WITH_DURING_OPERATOR (int): The value passed to the DURING operator is not a Date range literal
          INVALID_VALUE_WITH_LIKE_OPERATOR (int): A non-string value was passed to the LIKE operator.
          OPERATOR_FIELD_MISMATCH (int): An operator was provided that is inapplicable to the field being
          filtered.
          PROHIBITED_EMPTY_LIST_IN_CONDITION (int): A Condition was found with an empty list.
          PROHIBITED_ENUM_CONSTANT (int): A condition used in the query references an unsupported enum constant.
          PROHIBITED_FIELD_COMBINATION_IN_SELECT_CLAUSE (int): Fields that are not allowed to be selected together were included in
          the SELECT clause.
          PROHIBITED_FIELD_IN_ORDER_BY_CLAUSE (int): A field that is not orderable was included in the ORDER BY clause.
          PROHIBITED_FIELD_IN_SELECT_CLAUSE (int): A field that is not selectable was included in the SELECT clause.
          PROHIBITED_FIELD_IN_WHERE_CLAUSE (int): A field that is not filterable was included in the WHERE clause.
          PROHIBITED_RESOURCE_TYPE_IN_FROM_CLAUSE (int): Resource type specified in the FROM clause is not supported by this
          service.
          PROHIBITED_RESOURCE_TYPE_IN_SELECT_CLAUSE (int): A field that comes from an incompatible resource was included in the
          SELECT clause.
          PROHIBITED_RESOURCE_TYPE_IN_WHERE_CLAUSE (int): A field that comes from an incompatible resource was included in the
          WHERE clause.
          PROHIBITED_METRIC_IN_SELECT_OR_WHERE_CLAUSE (int): A metric incompatible with the main resource or other selected
          segmenting resources was included in the SELECT or WHERE clause.
          PROHIBITED_SEGMENT_IN_SELECT_OR_WHERE_CLAUSE (int): A segment incompatible with the main resource or other selected
          segmenting resources was included in the SELECT or WHERE clause.
          PROHIBITED_SEGMENT_WITH_METRIC_IN_SELECT_OR_WHERE_CLAUSE (int): A segment in the SELECT clause is incompatible with a metric in the
          SELECT or WHERE clause.
          LIMIT_VALUE_TOO_LOW (int): The value passed to the limit clause is too low.
          PROHIBITED_NEWLINE_IN_STRING (int): Query has a string containing a newline character.
          PROHIBITED_VALUE_COMBINATION_IN_LIST (int): List contains values of different types.
          PROHIBITED_VALUE_COMBINATION_WITH_BETWEEN_OPERATOR (int): The values passed to the BETWEEN operator are not of the same type.
          STRING_NOT_TERMINATED (int): Query contains unterminated string.
          TOO_MANY_SEGMENTS (int): Too many segments are specified in SELECT clause.
          UNEXPECTED_END_OF_QUERY (int): Query is incomplete and cannot be parsed.
          UNEXPECTED_FROM_CLAUSE (int): FROM clause cannot be specified in this query.
          UNRECOGNIZED_FIELD (int): Query contains one or more unrecognized fields.
          UNEXPECTED_INPUT (int): Query has an unexpected extra part.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        QUERY_ERROR = 50
        BAD_ENUM_CONSTANT = 18
        BAD_ESCAPE_SEQUENCE = 7
        BAD_FIELD_NAME = 12
        BAD_LIMIT_VALUE = 15
        BAD_NUMBER = 5
        BAD_OPERATOR = 3
        BAD_RESOURCE_TYPE_IN_FROM_CLAUSE = 45
        BAD_SYMBOL = 2
        BAD_VALUE = 4
        DATE_RANGE_TOO_WIDE = 36
        EXPECTED_AND = 30
        EXPECTED_BY = 14
        EXPECTED_DIMENSION_FIELD_IN_SELECT_CLAUSE = 37
        EXPECTED_FILTERS_ON_DATE_RANGE = 55
        EXPECTED_FROM = 44
        EXPECTED_LIST = 41
        EXPECTED_REFERENCED_FIELD_IN_SELECT_CLAUSE = 16
        EXPECTED_SELECT = 13
        EXPECTED_SINGLE_VALUE = 42
        EXPECTED_VALUE_WITH_BETWEEN_OPERATOR = 29
        INVALID_DATE_FORMAT = 38
        INVALID_STRING_VALUE = 57
        INVALID_VALUE_WITH_BETWEEN_OPERATOR = 26
        INVALID_VALUE_WITH_DURING_OPERATOR = 22
        INVALID_VALUE_WITH_LIKE_OPERATOR = 56
        OPERATOR_FIELD_MISMATCH = 35
        PROHIBITED_EMPTY_LIST_IN_CONDITION = 28
        PROHIBITED_ENUM_CONSTANT = 54
        PROHIBITED_FIELD_COMBINATION_IN_SELECT_CLAUSE = 31
        PROHIBITED_FIELD_IN_ORDER_BY_CLAUSE = 40
        PROHIBITED_FIELD_IN_SELECT_CLAUSE = 23
        PROHIBITED_FIELD_IN_WHERE_CLAUSE = 24
        PROHIBITED_RESOURCE_TYPE_IN_FROM_CLAUSE = 43
        PROHIBITED_RESOURCE_TYPE_IN_SELECT_CLAUSE = 48
        PROHIBITED_RESOURCE_TYPE_IN_WHERE_CLAUSE = 58
        PROHIBITED_METRIC_IN_SELECT_OR_WHERE_CLAUSE = 49
        PROHIBITED_SEGMENT_IN_SELECT_OR_WHERE_CLAUSE = 51
        PROHIBITED_SEGMENT_WITH_METRIC_IN_SELECT_OR_WHERE_CLAUSE = 53
        LIMIT_VALUE_TOO_LOW = 25
        PROHIBITED_NEWLINE_IN_STRING = 8
        PROHIBITED_VALUE_COMBINATION_IN_LIST = 10
        PROHIBITED_VALUE_COMBINATION_WITH_BETWEEN_OPERATOR = 21
        STRING_NOT_TERMINATED = 6
        TOO_MANY_SEGMENTS = 34
        UNEXPECTED_END_OF_QUERY = 9
        UNEXPECTED_FROM_CLAUSE = 47
        UNRECOGNIZED_FIELD = 32
        UNEXPECTED_INPUT = 11


class RecommendationErrorEnum(object):
    class RecommendationError(enum.IntEnum):
        """
        Enum describing possible errors from applying a recommendation.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          BUDGET_AMOUNT_TOO_SMALL (int): The specified budget amount is too low e.g. lower than minimum currency
          unit or lower than ad group minimum cost-per-click.
          BUDGET_AMOUNT_TOO_LARGE (int): The specified budget amount is too large.
          INVALID_BUDGET_AMOUNT (int): The specified budget amount is not a valid amount. e.g. not a multiple
          of minimum currency unit.
          POLICY_ERROR (int): The specified keyword or ad violates ad policy.
          INVALID_BID_AMOUNT (int): The specified bid amount is not valid. e.g. too many fractional digits,
          or negative amount.
          ADGROUP_KEYWORD_LIMIT (int): The number of keywords in ad group have reached the maximum allowed.
          RECOMMENDATION_ALREADY_APPLIED (int): The recommendation requested to apply has already been applied.
          RECOMMENDATION_INVALIDATED (int): The recommendation requested to apply has been invalidated.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        BUDGET_AMOUNT_TOO_SMALL = 2
        BUDGET_AMOUNT_TOO_LARGE = 3
        INVALID_BUDGET_AMOUNT = 4
        POLICY_ERROR = 5
        INVALID_BID_AMOUNT = 6
        ADGROUP_KEYWORD_LIMIT = 7
        RECOMMENDATION_ALREADY_APPLIED = 8
        RECOMMENDATION_INVALIDATED = 9


class RegionCodeErrorEnum(object):
    class RegionCodeError(enum.IntEnum):
        """
        Enum describing possible region code errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          INVALID_REGION_CODE (int): Invalid region code.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INVALID_REGION_CODE = 2


class RequestErrorEnum(object):
    class RequestError(enum.IntEnum):
        """
        Enum describing possible request errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          RESOURCE_NAME_MISSING (int): Resource name is required for this request.
          RESOURCE_NAME_MALFORMED (int): Resource name provided is malformed.
          BAD_RESOURCE_ID (int): Resource name provided is malformed.
          INVALID_CUSTOMER_ID (int): Customer ID is invalid.
          OPERATION_REQUIRED (int): Mutate operation should have either create, update, or remove specified.
          RESOURCE_NOT_FOUND (int): Requested resource not found.
          INVALID_PAGE_TOKEN (int): Next page token specified in user request is invalid.
          EXPIRED_PAGE_TOKEN (int): Next page token specified in user request has expired.
          REQUIRED_FIELD_MISSING (int): Required field is missing.
          IMMUTABLE_FIELD (int): The field cannot be modified because it's immutable. It's also possible
          that the field can be modified using 'create' operation but not 'update'.
          TOO_MANY_MUTATE_OPERATIONS (int): Received too many entries in request.
          CANNOT_BE_EXECUTED_BY_MANAGER_ACCOUNT (int): Request cannot be executed by a manager account.
          CANNOT_MODIFY_FOREIGN_FIELD (int): Mutate request was attempting to modify a readonly field.
          For instance, Budget fields can be requested for Ad Group,
          but are read-only for adGroups:mutate.
          INVALID_ENUM_VALUE (int): Enum value is not permitted.
          DEVELOPER_TOKEN_PARAMETER_MISSING (int): The developer-token parameter is required for all requests.
          LOGIN_CUSTOMER_ID_PARAMETER_MISSING (int): The login-customer-id parameter is required for this request.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        RESOURCE_NAME_MISSING = 3
        RESOURCE_NAME_MALFORMED = 4
        BAD_RESOURCE_ID = 17
        INVALID_CUSTOMER_ID = 16
        OPERATION_REQUIRED = 5
        RESOURCE_NOT_FOUND = 6
        INVALID_PAGE_TOKEN = 7
        EXPIRED_PAGE_TOKEN = 8
        REQUIRED_FIELD_MISSING = 9
        IMMUTABLE_FIELD = 11
        TOO_MANY_MUTATE_OPERATIONS = 13
        CANNOT_BE_EXECUTED_BY_MANAGER_ACCOUNT = 14
        CANNOT_MODIFY_FOREIGN_FIELD = 15
        INVALID_ENUM_VALUE = 18
        DEVELOPER_TOKEN_PARAMETER_MISSING = 19
        LOGIN_CUSTOMER_ID_PARAMETER_MISSING = 20


class SharedCriterionErrorEnum(object):
    class SharedCriterionError(enum.IntEnum):
        """
        Enum describing possible shared criterion errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CRITERION_TYPE_NOT_ALLOWED_FOR_SHARED_SET_TYPE (int): The criterion is not appropriate for the shared set type.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CRITERION_TYPE_NOT_ALLOWED_FOR_SHARED_SET_TYPE = 2


class SharedSetErrorEnum(object):
    class SharedSetError(enum.IntEnum):
        """
        Enum describing possible shared set errors.

        Attributes:
          UNSPECIFIED (int): Enum unspecified.
          UNKNOWN (int): The received error code is not known in this version.
          CUSTOMER_CANNOT_CREATE_SHARED_SET_OF_THIS_TYPE (int): The customer cannot create this type of shared set.
          DUPLICATE_NAME (int): A shared set with this name already exists.
          SHARED_SET_REMOVED (int): Removed shared sets cannot be mutated.
          SHARED_SET_IN_USE (int): The shared set cannot be removed because it is in use.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CUSTOMER_CANNOT_CREATE_SHARED_SET_OF_THIS_TYPE = 2
        DUPLICATE_NAME = 3
        SHARED_SET_REMOVED = 4
        SHARED_SET_IN_USE = 5
