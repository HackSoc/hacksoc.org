--
-- Implement a function which finds the maximum of two values.
-- For example
-- max' 2 3 => 3
-- max' 5 4 => 5
--
max' :: (Ord a) => a -> a -> a 
max' a b 
  | a > b = a
  | otherwise b


--
-- Find a function which finds the minimum of two values
-- For example
-- min' 2 3 => 2
-- min' 5 4 => 4
--
min' :: (Ord a) => a -> a -> a
min' a b
  | a > b = b
  | otherwise a

--
-- Implement the logical function "and"
-- For example
-- and' True False => False
-- and' True True => True
--
and' :: Bool -> Bool -> Bool
and' True x = x
and' False _ = False

--
-- Implement the logical function "or"
-- For example
-- or' False False => False
-- or' False True => True
--
or' :: Bool -> Bool -> Bool
or' False x = x
or' True _ = True

--
-- Implement the logical function "not" 
-- For example
-- not' False => True
--
not' :: Bool -> Bool
not' True = False
not' _ = True

--
-- Implement a function which adds two to any number it's given
-- For example
-- plusTwo 2 => 4
-- plusTwo 5 => 7
--
plusTwo :: (Num a) => a -> a
plusTwo = (+2)

--
-- Implement a function which adds two to every number of a list
-- For example
-- plusTwoList [1,2,3] => [3,4,5]
-- plusTwoList [100] => [102]
--
plusTwoList :: (Num a) => [a] -> [a]
plusTwoList = map plusTwo

--
-- Given the functions 'odd' and 'even' below, prove that they always terminate
-- for any positive integer, and that they always terminate with the correct 
-- answer
--
odd' :: (Num a) => a -> Bool
even' :: (Num a) => a -> Bool

even' 0 = True
even' n = odd' (n - 1)

odd' 0 = False
odd' n = even' (n - 1)


