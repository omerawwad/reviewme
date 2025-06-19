import React from "react";
import { HStack, Skeleton, SkeletonText, Stack } from "@chakra-ui/react";

function ItemsSkeleton() {
  return (
    <Stack gap="6" maxW="xs">
      <Skeleton height="30px" width="300px" />
      <Skeleton height="30px" />
    </Stack>
  );
}

export default ItemsSkeleton;
