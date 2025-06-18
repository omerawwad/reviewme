import {
  Box,
  HStack,
  Skeleton,
  SkeletonCircle,
  SkeletonText,
  Stack,
} from "@chakra-ui/react";

function ReviewsSkeleton() {
  return (
    <Stack gap="6" maxW="xs">
      <HStack width="full">
        {/* <SkeletonCircle size="10" /> */}
        <SkeletonText noOfLines={2} spacing="2" skeletonHeight="4" />
      </HStack>
      <Skeleton height="30px" width="300px" />
      <Skeleton height="30px" />
    </Stack>
  );
}

export default ReviewsSkeleton;
