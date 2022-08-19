    tic
    edgeListLocalLH=zeros(nfllen*3,2,'single');
    parfor i=1:nfllen
        [x1,~]=find(nfl==nfl(i,1));
        [x2,~]=find(nfl==nfl(i,2));
        [x3,~]=find(nfl==nfl(i,3));
        x=[x1;x2;x3];
        [~, I] = unique(x, 'first');
        tmp = 1:length(x);
        tmp(I) = [];
        x=x(tmp);
        x(x==i)=[];
        edgeListLocalLH(count,:)=[i,x(1)];
        count=count+1;
        edgeListLocalLH(count,:)=[i,x(2)];
        count=count+1;
        edgeListLocalLH(count,:)=[i,x(3)];
        count=count+1;
        clear x1 x2 x3 x I tmp
        if mod(i/1000,1)==0
            disp(num2str(nfllen\i))
        end
    end
    toc
    edgeListLocalRH=zeros(nfrlen*3,2,'single');
    count=1;
    tempVar = zeros(nfrlen, 3);
    parfor i=1:1:nfrlen
        [x1,~]=find(nfr==nfr(i,1));
        [x2,~]=find(nfr==nfr(i,2));
        [x3,~]=find(nfr==nfr(i,3));
        x=[x1;x2;x3];
        [~, I] = unique(x, 'first');
        tmp = 1:length(x);
        tmp(I) = [];
        x=x(tmp);
        x(x==i)=[];
        tempVar(i) = [i+nfllen,x(1)+nfllen; i+nfllen,x(2)+nfllen; i+nfllen,x(3)+nfllen];

        edgeListLocalRH(4,[1,2,3]) = tempVar(i);
        edgeListLocalRH(count,:)=[i+nfllen,x(1)+nfllen];
        count=count+1;
        edgeListLocalRH(count,:)=[i+nfllen,x(2)+nfllen];
        count=count+1;
        edgeListLocalRH(count,:)=[i+nfllen,x(3)+nfllen];
        count=count+1;
        clear x1 x2 x3 x I tmp
        if mod(i/1000,1)==0
            disp(num2str(nfrlen\i))
        end
    end
    edgeListLocalRH = tempVar;
    edgeListLocal=[edgeListLocalLH;edgeListLocalRH];