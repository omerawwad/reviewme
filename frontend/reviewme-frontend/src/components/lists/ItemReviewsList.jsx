import ReviewsSkeleton from "../../pages/stillPages/ReviewsSkeleton";
import PaginationControls from "../smallComponents/PaginationControls";
import Review from "../objects/Review";

import "../../styles/ItemReviewsList.css";

function ItemReviewsList({
  reviews,
  pageInfo,
  setPage,
  refetch,
  error,
  loading,
}) {
  if (loading && pageInfo.current === 1) return <ItemReviewsList.Skeleton />;
  if (error) return <div>Error: {error}</div>;

  //   console.log("ItemReviewsList", reviews, pageInfo);
  return (
    <div className="item-reviews-list">
      <span className="reviews-list-title">Reviews</span>
      {reviews.map((review) => (
        <Review review={review} key={review.id} />
      ))}
      <PaginationControls
        pageInfo={pageInfo}
        setPage={setPage}
        refetch={refetch}
      />
    </div>
  );
}

ItemReviewsList.Skeleton = function ReviewsListSkeleton() {
  return (
    <div className="reviews-list-skeleton">
      {Array.from({ length: 3 }).map((_, index) => (
        <ReviewsSkeleton key={index} />
      ))}
    </div>
  );
};

export default ItemReviewsList;
