
#[derive(Debug, PartialEq, Clone, Eq)]
struct Pair<L,R> {
    left: L,
    right: R,
}

impl<L, R> Pair<L, R> {
    fn new(left:L, right:R) -> Self {
        let pair = Self { left, right };
        pair
    }

    fn swap(&self) -> Pair<R, L>
    where
        L: Clone,
        R: Clone,
    {
        Pair {
            left: self.right.clone(),
            right: self.left.clone(),
        }
    }

    fn map_right<F, U>(&self, mapper: F) -> Pair<L, U>
    where
        F: FnOnce(&R) -> U,
        U: Clone,
        L: Clone,

    {
        Pair {
            left: self.left.clone(),
            right: mapper(&self.right),
        }
    }

    fn map_left<F, T>(&self, mapper: F) -> Pair<T, R>
    where
        F: FnOnce(&L) -> T,
        T: Clone,
        R: Clone,
    {
        Pair {
            left: mapper(&self.left),
            right: self.right.clone(),
        }
    }
}

impl<L: Default, R: Default> Default for  Pair<L, R> {
    fn default() -> Self {
        Self {
            left: L::default(),
            right: R::default(),
        }
    }
}

impl<T: Clone> Pair<T, T> {
    pub fn to_vec(&self) -> Vec<T> {
        vec![self.left.clone(), self.right.clone()]
    }

    pub fn to_array(&self) -> [T; 2] {
        [self.left.clone(), self.right.clone()]
    }
}



fn main() {
    let pair = Pair::new("🦜", 1);
    println!("{:?}", pair);
    println!("{:?}", pair.swap());
    println!("{:?}", pair.map_left(|_| 1));
    println!(
        "{:?}",
        pair.map_right(|x| {
            let bytes = [239, 158, 165, 155];
            let bytes = bytes.into_iter().map(|b| b + x).collect::<Vec<_>>();
            String::from_utf8(bytes)
        })
    );
}
