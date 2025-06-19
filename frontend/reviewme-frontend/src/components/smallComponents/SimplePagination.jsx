import React from "react";
import { ButtonGroup, IconButton, Pagination } from "@chakra-ui/react";
import { LuChevronLeft, LuChevronRight } from "react-icons/lu";
function SimplePagination({ pageInfo, handlePageChange }) {
  // console.log("SimplePagination rendered with pageInfo:", pageInfo);
  return (
    <div className="pagination-controls">
      <Pagination.Root
        count={pageInfo.total_items}
        pageSize={pageInfo.page_size}
        page={pageInfo.current}
        onPageChange={(p) => {
          handlePageChange(p.page);
        }}
        colorPalette="gray"
      >
        <ButtonGroup variant="ghost" size="sm">
          <Pagination.PrevTrigger asChild>
            <IconButton>
              <LuChevronLeft />
            </IconButton>
          </Pagination.PrevTrigger>

          <Pagination.Items
            render={(page) => (
              <IconButton variant={{ base: "ghost", _selected: "solid" }}>
                {page.value}
              </IconButton>
            )}
          />

          <Pagination.NextTrigger asChild>
            <IconButton>
              <LuChevronRight />
            </IconButton>
          </Pagination.NextTrigger>
        </ButtonGroup>
      </Pagination.Root>
    </div>
  );
}

export default SimplePagination;
