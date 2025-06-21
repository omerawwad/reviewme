import { ButtonGroup, IconButton, Pagination } from "@chakra-ui/react";
import { LuChevronLeft, LuChevronRight } from "react-icons/lu";
import { Provider } from "../ui/provider";
import { useEffect, useState } from "react";
import "../../styles/PaginationControls.css";
import { LightMode } from "../ui/color-mode";
function PaginationControls({ pageInfo, setPage, refetch }) {
  //   console.log("PaginationControls rendered with pageInfo:", pageInfo);
  const [isUpdated, setIsUpdated] = useState(false);
  const handlePageChange = (selectedPage) => {
    const newPage = selectedPage.page;
    // console.log("New page selected:", newPage);
    // console.log("Current page info:", pageInfo);
    if (newPage < 1 || newPage > pageInfo.total) {
      console.warn("Invalid page number:", newPage);
      return;
    }
    setPage(newPage);
    setIsUpdated(true);
  };

  useEffect(() => {
    if (isUpdated) {
      //   console.log("Refetching data due to page update");
      refetch();
      setIsUpdated(false);
    }
  }, [isUpdated]);
  if (pageInfo.total_pages <= 1) {
    return null;
  }
  return (
    <div className="pagination-controls">
      <Pagination.Root
        count={pageInfo.totalReviews}
        pageSize={pageInfo.size}
        page={pageInfo.current}
        onPageChange={handlePageChange}
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

export default PaginationControls;
