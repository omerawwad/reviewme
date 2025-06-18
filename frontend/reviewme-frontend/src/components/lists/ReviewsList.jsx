import React from "react";
import useReviews from "../../hooks/useReviews";
import Review from "../objects/Review";
import PaginationControls from "../smallComponents/PaginationControls";
import ReviewsSkeleton from "../../pages/stillPages/ReviewsSkeleton";

import "../../styles/ReviewsList.css";
function ReviewsList() {
  const { reviews, loading, error, pageInfo, refetch, setPage } = useReviews();
  if (loading) return <ReviewsList.Skeleton />;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="reviews-list">
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

ReviewsList.Skeleton = function ReviewsListSkeleton() {
  return (
    <div className="reviews-list-skeleton">
      {Array.from({ length: 3 }).map((_, index) => (
        <ReviewsSkeleton key={index} />
      ))}
    </div>
  );
};

export default ReviewsList;
