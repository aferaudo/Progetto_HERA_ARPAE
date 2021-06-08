USE [Hera]
GO

/****** Object:  Table [dbo].[coord]    Script Date: 6/8/2021 10:40:01 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[coord](
	[cod_pozzo] [nvarchar](50) NOT NULL,
	[lat] [float] NOT NULL,
	[long] [float] NOT NULL,
 CONSTRAINT [PK_coord] PRIMARY KEY CLUSTERED 
(
	[cod_pozzo] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


