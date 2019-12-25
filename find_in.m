function circle = find_in(path)

file = dir([path,'*.his']);
circle = cell(size(file,1),1);
% figure
for i = 1:size(file,1)
    %% calculate center and radius
    disp(file(i).name)
    [im,~] = readHISfile([path,file(i).name]);
    [centerss, radiis, ~] = imfindcircles(im,[30 40]);
    disp(radiis)
    circle(i,:) = {[i,centerss,radiis]};
%     X = (centerss(1) - centersb(1))*260/1024;
%     Y = (centerss(2) - centersb(2))*260/1024;
    %% Plot
%     subplot(2,4,i);
%     imshow(im(300:1024-300,300:1024-300),[]);
%     hold on;
%     plot(centerss(1)-300,centerss(2)-300,'b+','LineWidth',1);
%     hold on;
%     plot(centersb(1)-300,centersb(2)-300,'g+','LineWidth',1);
%     hold on;
%     viscircles(centerss-300, radiis,'EdgeColor','b','LineWidth',0.5);
%     hold on;
%     viscircles(centersb-300, radiib,'EdgeColor','g','LineWidth',0.5);
%     disp(X);
%     disp(Y);

end
end